import json
from app.core.redis_client import redis_client
from typing import Dict, Any
import os

# Initialize Redis client (typically configured centrally).

async def get_revenue_summary(property_id: str, tenant_id: str, month: str) -> Dict[str, Any]:
    """
    Fetches revenue summary, utilizing caching to improve performance.
    """
    cache_key = f"revenue:{tenant_id}:{property_id}:{month}"
    
    # Try to get from cache
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Revenue calculation is delegated to the reservation service.
    from app.services.reservations import calculate_total_revenue
    
    # Calculate revenue
    result = await calculate_total_revenue(property_id, tenant_id, month)
    
    # Cache the result for 5 minutes
    await redis_client.set(cache_key, json.dumps(result), 300)
    
    return result
