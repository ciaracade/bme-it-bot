from datetime import datetime, timedelta
from typing import Dict, Optional
import asyncio

class RateLimiter:
    def __init__(self, requests_per_minute: int = 30):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = {}
        
    async def check_rate_limit(self, key: str) -> Optional[float]:
        """
        Check if request should be rate limited.
        Returns seconds to wait if limited, None if not limited.
        """
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)
        
        # Initialize or clean old requests
        if key not in self.requests:
            self.requests[key] = []
        self.requests[key] = [t for t in self.requests[key] if t > minute_ago]
        
        # Check limit
        if len(self.requests[key]) >= self.requests_per_minute:
            oldest = self.requests[key][0]
            wait_time = (oldest + timedelta(minutes=1) - now).total_seconds()
            return max(0, wait_time)
        
        # Add new request
        self.requests[key].append(now)
        return None

    async def wait_if_needed(self, key: str):
        """Wait if rate limited"""
        wait_time = await self.check_rate_limit(key)
        if wait_time:
            await asyncio.sleep(wait_time) 