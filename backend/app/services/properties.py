from typing import Dict, Any, List

from sqlalchemy import text

from app.core.database_pool import db_pool

async def get_properties(tenant_id: str) -> List[Dict[str, Any]]:
    """
    Lists the properties that belong to a tenant.
    """
    async with db_pool.get_session() as session:
        result = await session.execute(
            text("SELECT id, name FROM properties WHERE tenant_id = :tenant_id ORDER BY id"),
            {"tenant_id": tenant_id},
        )
        return [dict(row) for row in result.mappings().all()]