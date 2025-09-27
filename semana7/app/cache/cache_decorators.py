from functools import wraps
from .redis_config import cache_manager
import hashlib
import json
import asyncio

def cache_result(ttl_type: str = 'frequent_data', key_prefix: str = ""):
    def decorator(func):
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            func_name = func.__name__
            args_str = json.dumps({'args': args, 'kwargs': kwargs}, default=str)
            key_hash = hashlib.md5(args_str.encode()).hexdigest()[:8]
            cache_key = f"{key_prefix}:{func_name}:{key_hash}"

            cached = cache_manager.get_cache(cache_key)
            if cached is not None:
                return cached

            result = func(*args, **kwargs)
            cache_manager.set_cache(cache_key, result, category='data', ttl_type=ttl_type)
            return result

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            func_name = func.__name__
            args_str = json.dumps({'args': args, 'kwargs': kwargs}, default=str)
            key_hash = hashlib.md5(args_str.encode()).hexdigest()[:8]
            cache_key = f"{key_prefix}:{func_name}:{key_hash}"

            cached = cache_manager.get_cache(cache_key)
            if cached is not None:
                return cached

            result = await func(*args, **kwargs)
            cache_manager.set_cache(cache_key, result, category='data', ttl_type=ttl_type)
            return result

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    return decorator
