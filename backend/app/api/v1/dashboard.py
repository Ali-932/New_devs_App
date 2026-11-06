from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, Any, List
from app.services.cache import get_revenue_summary
from app.services.properties import get_properties
from app.core.auth import authenticate_request as get_current_user

router = APIRouter()

@router.get("/dashboard/summary")
async def get_dashboard_summary(
    property_id: str,
    month: str = Query(..., pattern=r"^\d{4}-(0[1-9]|1[0-2])$"),
    current_user: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    
    tenant_id = current_user.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=403, detail="No tenant access")

    revenue_data = await get_revenue_summary(property_id, tenant_id, month)
    

    return {
        "property_id": revenue_data['property_id'],
        "total_revenue": revenue_data['total'],
        "currency": revenue_data['currency'],
        "reservations_count": revenue_data['count']
    }

@router.get("/properties")
async def get_dashboard_properties(
    current_user: dict = Depends(get_current_user)
) -> List[Dict[str, Any]]:

    tenant_id = current_user.tenant_id
    if not tenant_id:
        raise HTTPException(status_code=403, detail="No tenant access")

    return await get_properties(tenant_id)
