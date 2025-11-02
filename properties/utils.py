from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging
logger = logging.getLogger(__name__)

def get_all_properties():
    properties = cache.get('all_properties')
    if properties is None:
        properties = Property.objects.all()
        cache.set('all_properties', properties, 3600)
    return properties

def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit and miss metrics and calculate hit ratio.
    """
    try:
        redis_conn = get_redis_connection("default")
        info = redis_conn.info()

        keyspace_hits = info.get("keyspace_hits", 0)
        keyspace_misses = info.get("keyspace_misses", 0)

        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = (keyspace_hits / total_requests) if total_requests > 0 else 0

        logger.info(f"Redis Cache Metrics → Hits: {keyspace_hits}, Misses: {keyspace_misses}, Hit Ratio: {hit_ratio}")

        return {
            "hits": keyspace_hits,
            "misses": keyspace_misses,
            "hit_ratio": hit_ratio,
        }

    except Exception as e:
        logger.error(f"Error retrieving Redis metrics: {e}")
        return {"error": str(e)}
