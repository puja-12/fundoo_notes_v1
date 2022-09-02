import redis
import json
from django.conf import  settings

redis_cache = redis.Redis(**settings.CACHES)


class RedisFunction:

    @staticmethod
    def get_key(key):
        return redis_cache.get(key)

    @staticmethod
    def set_key(key, cache_data):
        return redis_cache.set(key, cache_data)