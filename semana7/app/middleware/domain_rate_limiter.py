from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import redis
import time

class DomainRateLimiter(BaseHTTPMiddleware):
    def __init__(self, app, domain_prefix: str = 'bakery_', redis_client: redis.Redis = None):
        super().__init__(app)
        self.domain_prefix = domain_prefix
        self.redis = redis_client or redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        self.rate_limits = {
            "inventory": {"requests": 300, "window": 60},
            "sales": {"requests": 200, "window": 60},
            "production": {"requests": 150, "window": 60},
            "general": {"requests": 150, "window": 60},
            "admin": {"requests": 50, "window": 60}
        }

    def _get_rate_limit_category(self, path: str, method: str) -> str:
        if "/stock" in path or "/inventory" in path:
            return "inventory"
        if "/venta" in path or "/sales" in path:
            return "sales"
        if "/produccion" in path:
            return "production"
        if "/admin" in path:
            return "admin"
        return "general"

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if not path.startswith(f"/{self.domain_prefix.rstrip('_')}"):
            return await call_next(request)

        client_ip = request.client.host if request.client else 'unknown'
        category = self._get_rate_limit_category(path, request.method)
        config = self.rate_limits.get(category, self.rate_limits['general'])

        now = int(time.time())
        window_start = now - config['window']
        key = f"{self.domain_prefix}:rate_limit:{category}:{client_ip}"

        requests = self.redis.zrangebyscore(key, window_start, now)
        if len(requests) >= config['requests']:
            raise HTTPException(status_code=429, detail={
                "error": "Rate limit exceeded",
                "category": category,
                "limit": config['requests']
            })

        self.redis.zadd(key, {str(now): now})
        self.redis.expire(key, config['window'])
        self.redis.zremrangebyscore(key, 0, window_start)

        response = await call_next(request)
        return response
