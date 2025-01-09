import json
from datetime import datetime, timedelta
from typing import Any, Dict
import aioredis
from .config import get_settings
import logging

settings = get_settings()
logger = logging.getLogger(__name__)

class RedisLogger:
    def __init__(self):
        self.redis = None
        self.log_ttl = 7 * 24 * 60 * 60  # 7 days in seconds
        self.max_logs = 10000  # Maximum number of logs to keep

    async def connect(self):
        """Connect to Redis"""
        try:
            if not self.redis:
                logger.debug(f"Connecting to Redis at {settings.REDIS_URL}")
                self.redis = await aioredis.from_url(
                    settings.REDIS_URL,
                    encoding="utf-8",
                    decode_responses=True
                )
                logger.debug("Successfully connected to Redis")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise

    async def log(self, level: str, message: str, **kwargs):
        """Add log entry to Redis"""
        try:
            await self.connect()
            
            # Create log entry
            log_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "level": level,
                "message": message,
                **kwargs
            }
            
            # Convert to JSON string
            log_json = json.dumps(log_entry)
            logger.debug(f"Preparing to log to Redis: {log_json[:200]}...")
            
            async with self.redis.pipeline() as pipe:
                # Add to sorted set with score as timestamp
                timestamp = datetime.utcnow().timestamp()
                await pipe.zadd("application_logs", {log_json: timestamp})
                
                # Add to level-specific list
                await pipe.lpush(f"logs:{level.lower()}", log_json)
                
                # If request_id exists, add to request-specific list
                if "request_id" in kwargs:
                    request_id = kwargs["request_id"]
                    await pipe.lpush(f"logs:request:{request_id}", log_json)
                    await pipe.expire(f"logs:request:{request_id}", 24 * 60 * 60)
                
                # Trim old entries
                await pipe.zremrangebyrank("application_logs", 0, -self.max_logs-1)
                await pipe.ltrim(f"logs:{level.lower()}", 0, self.max_logs)
                
                # Execute pipeline
                await pipe.execute()
                logger.debug("Successfully logged to Redis")
                
        except Exception as e:
            logger.error(f"Failed to log to Redis: {e}")
            raise

    async def get_logs(self, level: str = None, request_id: str = None,
                      start_time: datetime = None, end_time: datetime = None,
                      limit: int = 100) -> list:
        """Retrieve logs from Redis"""
        try:
            await self.connect()
            
            if request_id:
                logger.debug(f"Fetching logs for request_id: {request_id}")
                logs = await self.redis.lrange(f"logs:request:{request_id}", 0, -1)
            elif level:
                logger.debug(f"Fetching logs for level: {level}")
                logs = await self.redis.lrange(f"logs:{level.lower()}", 0, limit-1)
            else:
                logger.debug("Fetching logs by time range")
                if not start_time:
                    start_time = datetime.utcnow() - timedelta(hours=1)
                if not end_time:
                    end_time = datetime.utcnow()
                    
                start_ts = start_time.timestamp()
                end_ts = end_time.timestamp()
                
                logs = await self.redis.zrangebyscore(
                    "application_logs",
                    min=start_ts,
                    max=end_ts,
                    start=0,
                    num=limit
                )
            
            logger.debug(f"Found {len(logs)} logs")
            return [json.loads(log) for log in logs]
            
        except Exception as e:
            logger.error(f"Failed to retrieve logs from Redis: {e}")
            raise

# Global Redis logger instance
redis_logger = RedisLogger() 