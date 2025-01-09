import time
import json
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.concurrency import iterate_in_threadpool
from .logger import setup_logger
from .metrics import update_metrics
from .redis_logger import redis_logger
import asyncio
import traceback

logger = setup_logger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Start timer
        start_time = time.time()
        
        try:
            # Log request directly to Redis
            body = ""
            if request.method in ["POST", "PUT", "PATCH"]:
                try:
                    raw_body = await request.body()
                    await request.body()  # Reset body stream
                    if raw_body:
                        body = raw_body.decode()
                except Exception:
                    body = "(unable to decode body)"

            await redis_logger.log(
                level="INFO",
                message=f"Request {request.method} {request.url.path}",
                request_id=request_id,
                request={
                    "method": request.method,
                    "url": str(request.url),
                    "path": request.url.path,
                    "headers": dict(request.headers),
                    "path_params": request.path_params,
                    "query_params": str(request.query_params),
                    "body": body,
                    "client": request.client.host if request.client else None,
                    "user_agent": request.headers.get("user-agent")
                }
            )
            
            # Process request
            response = await call_next(request)
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            
            # Calculate metrics
            process_time = (time.time() - start_time) * 1000
            update_metrics(request.method, str(request.url.path), response.status_code, process_time)
            
            # Log response directly to Redis
            response_body = ""
            if not response.headers.get("content-encoding", ""):
                response_body = [section async for section in response.body_iterator]
                response.body_iterator = iterate_in_threadpool(iter(response_body))
                response_body = b"".join(response_body).decode()

            await redis_logger.log(
                level="INFO",
                message=f"Response {response.status_code} for {request.method} {request.url.path}",
                request_id=request_id,
                response={
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "body": response_body if len(response_body) < 1000 else "(body too large)",
                    "process_time_ms": round(process_time, 2)
                }
            )
            
            return response
            
        except Exception as e:
            # Log error directly to Redis
            process_time = (time.time() - start_time) * 1000
            await redis_logger.log(
                level="ERROR",
                message=f"Request failed: {str(e)}",
                request_id=request_id,
                error={
                    "type": type(e).__name__,
                    "message": str(e),
                    "traceback": traceback.format_exc()
                },
                request={
                    "method": request.method,
                    "url": str(request.url),
                    "process_time_ms": round(process_time, 2)
                }
            )
            raise 