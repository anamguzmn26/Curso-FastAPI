import redis
import json
import os
from typing import Optional, Any

class DomainCacheConfig:
    def __init__(self, domain_prefix: str = "bakery_"):
        self.domain_prefix = domain_prefix
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=0,
            decode_responses=True
        )
        self.cache_ttl = {
            'frequent_data': 60,     # 60s para stock en tiempo real
            'stable_data': 3600,     # 1h
            'reference_data': 86400, # 24h para recetas/catalogo
            'temp_data': 30
        }

    def get_cache_key(self, category: str, identifier: str) -> str:
        ident = str(identifier) if identifier is not None else ''
        return f"{self.domain_prefix}{category}:{ident}"

    def set_cache(self, key: str, value: Any, category: str = 'data', ttl_type: str = 'frequent_data') -> bool:
        try:
            cache_key = self.get_cache_key(category, key)
            serialized_value = json.dumps(value, default=str)
            ttl = self.cache_ttl.get(ttl_type, 60)
            self.redis_client.setex(cache_key, ttl, serialized_value)
            return True
        except Exception as e:
            print(f"Error setting cache: {e}")
            return False

    def get_cache(self, key: str, category: str = 'data') -> Optional[Any]:
        try:
            cache_key = self.get_cache_key(category, key)
            cached_value = self.redis_client.get(cache_key)
            if cached_value:
                return json.loads(cached_value)
            return None
        except Exception as e:
            print(f"Error getting cache: {e}")
            return None

    def invalidate_cache(self, pattern: str = None):
        try:
            if pattern:
                cache_pattern = f"{self.domain_prefix}*{pattern}*"
            else:
                cache_pattern = f"{self.domain_prefix}*"
            keys = [k for k in self.redis_client.scan_iter(match=cache_pattern)]
            if keys:
                self.redis_client.delete(*keys)
        except Exception as e:
            print(f"Error invalidating cache: {e}")

# instancia global
cache_manager = DomainCacheConfig()
