from collections import defaultdict
from statistics import mean
from threading import Lock
import time

class Metrics:
    def __init__(self):
        self.lock = Lock()
        self.requests = defaultdict(list)
        self.status_codes = defaultdict(int)
        self.endpoints = defaultdict(int)
        self.response_times = defaultdict(list)
        
    def update(self, method: str, path: str, status_code: int, response_time: float):
        with self.lock:
            key = f"{method} {path}"
            self.requests[key].append(time.time())
            self.status_codes[status_code] += 1
            self.endpoints[key] += 1
            self.response_times[key].append(response_time)
            
            # Clean old requests (older than 1 hour)
            cutoff = time.time() - 3600
            self.requests[key] = [t for t in self.requests[key] if t > cutoff]
    
    def get_stats(self):
        with self.lock:
            stats = {
                "requests_per_endpoint": dict(self.endpoints),
                "status_codes": dict(self.status_codes),
                "response_times": {
                    endpoint: {
                        "min": min(times),
                        "max": max(times),
                        "avg": mean(times),
                        "count": len(times)
                    }
                    for endpoint, times in self.response_times.items()
                    if times
                },
                "requests_last_hour": {
                    endpoint: len(times)
                    for endpoint, times in self.requests.items()
                }
            }
            return stats

# Global metrics instance
_metrics = Metrics()

def update_metrics(method: str, path: str, status_code: int, response_time: float):
    """Update global metrics"""
    _metrics.update(method, path, status_code, response_time)

def get_metrics():
    """Get current metrics"""
    return _metrics.get_stats() 