import time
from typing import Dict, Tuple
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

class RateLimiter(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.request_records: Dict[str, list] = {}
        
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        
        # Check if client has exceeded rate limit
        if self._is_rate_limited(client_ip):
            return Response(
                content="Rate limit exceeded. Please try again later.",
                status_code=HTTP_429_TOO_MANY_REQUESTS
            )
        
        # Process the request
        response = await call_next(request)
        return response
    
    def _is_rate_limited(self, client_ip: str) -> bool:
        """Check if the client has exceeded the rate limit."""
        current_time = time.time()
        
        # Initialize record for new clients
        if client_ip not in self.request_records:
            self.request_records[client_ip] = []
        
        # Remove old records outside the current window
        self.request_records[client_ip] = [
            timestamp for timestamp in self.request_records[client_ip]
            if current_time - timestamp <= self.window_seconds
        ]
        
        # Check if client has reached the limit
        if len(self.request_records[client_ip]) >= self.max_requests:
            return True
        
        # Record this request
        self.request_records[client_ip].append(current_time)
        return False 