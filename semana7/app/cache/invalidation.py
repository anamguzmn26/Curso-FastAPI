from .redis_config import cache_manager

class DomainCacheInvalidation:
    @staticmethod
    def on_entity_update(entity_id: str, entity_type: str):
        patterns = [f"{entity_type}", "frequent_queries", "stock", "data_"]
        for p in patterns:
            cache_manager.invalidate_cache(p)

    @staticmethod
    def on_catalog_update():
        cache_manager.invalidate_cache('catalog')
