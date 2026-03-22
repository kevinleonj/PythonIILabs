from typing import Any, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models import User, Station
from src.app.security import get_current_user
from src.app.schemas.stations import StationCreate, StationResponse
from src.app.logger import logger

router = APIRouter()


@router.post("/", response_model=StationResponse, status_code=201)
async def create_station(
    station_data: StationCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Any:
    logger.info(f"Station creation requested by user: {current_user.username}")
    if current_user.role != "admin":
        logger.warning(f"Non-admin user {current_user.username} tried to create a station")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create stations",
        )

    new_station = Station(**station_data.model_dump())
    db.add(new_station)
    await db.commit()
    await db.refresh(new_station)
    logger.info(f"Station created: {new_station.name} (id: {new_station.id})")
    return new_station