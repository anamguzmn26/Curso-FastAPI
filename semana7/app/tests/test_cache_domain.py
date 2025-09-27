import pytest
from app.cache.redis_config import cache_manager

def test_basic_set_get():
    key = 'unittest_key'
    data = {'id':1,'nombre':'Panadero'}
    assert cache_manager.set_cache(key, data)
    val = cache_manager.get_cache(key)
    assert val == data
    cache_manager.invalidate_cache(key)
