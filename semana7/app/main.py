from fastapi import FastAPI
import redis
from .middleware.domain_rate_limiter import DomainRateLimiter
from .middleware.domain_logger import DomainLogger
from .middleware.domain_validator import DomainValidator
from .routers import products

DOMAIN_PREFIX = 'bakery_'
app = FastAPI(title=f"API Panaderia - {DOMAIN_PREFIX}")

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

app.add_middleware(DomainValidator, domain_prefix=DOMAIN_PREFIX)
app.add_middleware(DomainLogger, domain_prefix=DOMAIN_PREFIX)
app.add_middleware(DomainRateLimiter, domain_prefix=DOMAIN_PREFIX, redis_client=redis_client)

app.include_router(products.router)
