from datetime import datetime
from decimal import Decimal
from typing import Dict, Any, List, Optional

async def calculate_total_revenue(property_id: str, tenant_id: str, month: Optional[str] = None) -> Dict[str, Any]:
    """
    Aggregates a property's total revenue, all-time by default.
    Pass month as YYYY-MM to limit it to that month, in the property's timezone.
    """
    try:
        # Import database pool
        from app.core.database_pool import db_pool

        if db_pool.session_factory:
            async with db_pool.get_session() as session:
                # Use SQLAlchemy text for raw SQL
                from sqlalchemy import text
                
                query = """
                    SELECT
                        property_id,
                        ROUND(SUM(total_amount), 2) as total_revenue,
                        COUNT(*) as reservation_count
                    FROM reservations
                    WHERE property_id = :property_id AND tenant_id = :tenant_id
                """
                params = {"property_id": property_id, "tenant_id": tenant_id}

                if month:
                    query += """
                    AND to_char(check_in_date AT TIME ZONE (
                        SELECT timezone FROM properties WHERE id = :property_id AND tenant_id = :tenant_id
                    ), 'YYYY-MM') = :month
                    """
                    params["month"] = month

                query += " GROUP BY property_id"

                result = await session.execute(text(query), params)
                row = result.fetchone()
                
                if row:
                    total_revenue = Decimal(str(row.total_revenue))
                    return {
                        "property_id": property_id,
                        "tenant_id": tenant_id,
                        "total": str(total_revenue),
                        "currency": "USD", 
                        "count": row.reservation_count
                    }
                else:
                    # No reservations found for this property
                    return {
                        "property_id": property_id,
                        "tenant_id": tenant_id,
                        "total": "0.00",
                        "currency": "USD",
                        "count": 0
                    }
        else:
            raise Exception("Database pool not available")
            
    except Exception as e:
        print(f"Database error for {property_id} (tenant: {tenant_id}): {e}")
