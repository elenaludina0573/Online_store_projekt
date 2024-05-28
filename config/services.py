from django.conf import settings
from django.core.cache import cache


def get_key(name):
    """"Возвращает ключ для кеширования"""
    redis_cache_key = '_cache'
    return f'{name}{redis_cache_key}'


def get_cached_data(model):
    if not settings.CACHE_ENABLED:
        return model.objects.all()
    key = get_key(model.__name__)
    model_data = cache.get(key)
    if model_data:
        return model_data
    model_data = model.objects.all()
    cache.set(key, model_data)
    return model_data
