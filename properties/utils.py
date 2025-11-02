from django.core.cache import cache
from .models import Property

def get_all_properties():
    cached_properties = cache.get('all_properties')
    if cached_properties is not None:
        return cached_properties

    queryset = list(Property.objects.values())
    cache.set('all_properties', queryset, 3600)  # 1 hour
    return queryset
