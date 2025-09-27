from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime

class DomainValidator(BaseHTTPMiddleware):
    def __init__(self, app, domain_prefix: str = 'bakery_'):
        super().__init__(app)
        self.domain_prefix = domain_prefix
        self.validators = {
            'required_headers': ['X-Bakery-Auth'],
            'business_hours': (5, 22)  # 5:00 - 22:00
        }

    def _validate_business_hours(self, path: str) -> bool:
        if '/produccion' in path:
            return True  # producción puede ser 24/7 si así lo decides
        h = datetime.now().hour
        start, end = self.validators['business_hours']
        return start <= h <= end

    def _validate_required_headers(self, request: Request) -> bool:
        for h in self.validators['required_headers']:
            if h not in request.headers:
                return False
        return True

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if not path.startswith(f"/{self.domain_prefix.rstrip('_')}"):
            return await call_next(request)

        if not self._validate_business_hours(path):
            raise HTTPException(status_code=403, detail={"error": "Fuera de horario de atención"})

        if not self._validate_required_headers(request):
            raise HTTPException(status_code=400, detail={"error": "Header X-Bakery-Auth requerido"})

        return await call_next(request)
