from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time
import json
import os

class DomainLogger(BaseHTTPMiddleware):
    def __init__(self, app, domain_prefix: str = 'bakery_'):
        super().__init__(app)
        self.domain_prefix = domain_prefix
        self.logger = logging.getLogger(f"{domain_prefix}domain_logger")
        self.logger.setLevel(logging.INFO)
        os.makedirs('logs', exist_ok=True)
        handler = logging.FileHandler(f"logs/{domain_prefix}domain.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(handler)
        self.logged_endpoints = {"/update-stock": "WARNING", "/venta": "INFO"}

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if not path.startswith(f"/{self.domain_prefix.rstrip('_')}"):
            return await call_next(request)

        should_log = any(pat in path for pat in self.logged_endpoints.keys())
        if should_log:
            start = time.time()
            self.logger.info(f"REQUEST_START: {json.dumps({'path': path, 'method': request.method})}")

        response = await call_next(request)

        if should_log:
            duration = time.time() - start
            self.logger.info(f"REQUEST_END: {{'path': '{path}', 'status': {response.status_code}, 'duration': {duration}}}")

        return response
