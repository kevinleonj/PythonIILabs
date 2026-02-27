from typing import Any
from fastapi import APIRouter, Depends, Header, HTTPException

def verify_admin_key(
        api_key: str = Header(...),
) -> None:
    correct_key = "eco-admin-secret"

    if api_key != correct_key:
        raise HTTPException(
            status_code = 403,
            detail="Forbidden: invalid API key"
        )
    
router = APIRouter(
    dependencies = [Depends(verify_admin_key)]
)

@router.get("/stats")
def get_admin_stats() -> Any:
    return {
        "total bikes": 3,
        "active_rentals": 1,
        "message": "You are authorized to see this"
    }