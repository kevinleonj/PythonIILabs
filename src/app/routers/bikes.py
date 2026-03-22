from typing import Any, Optional, Literal
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import get_db
from src.models import Bike
from src.app.schemas.bikes import BikeCreate, BikeResponse
from src.app.logger import logger

router = APIRouter()


@router.get("/", response_model=list[BikeResponse])
async def get_all_bikes(
    status: Optional[Literal["available", "rented", "maintenance"]] = None,
    db: AsyncSession = Depends(get_db),
) -> Any:
    logger.info("Fetching all bikes")
    result = await db.execute(select(Bike))
    all_bikes = result.scalars().all()
    if status is not None:
        filtered_bikes = [bike for bike in all_bikes if bike.status == status]
        if not filtered_bikes:
            logger.warning("No bikes found with status: %s", status)
        return filtered_bikes
    if not all_bikes:
        logger.warning("No bikes found")
    return all_bikes


@router.get("/{bike_id}", response_model=BikeResponse)
async def get_bike(
    bike_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    bike = await db.get(Bike, bike_id)
    if bike is None:
        raise HTTPException(status_code=404, detail="Bike not found")
    return bike


@router.post("/", response_model=BikeResponse, status_code=201)
async def create_bike(
    new_bike: BikeCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    logger.info("Creating new bike: %s", new_bike.model)
    created_bike = Bike(**new_bike.model_dump())
    db.add(created_bike)
    await db.commit()
    await db.refresh(created_bike)
    return created_bike


@router.put("/{bike_id}", response_model=BikeResponse)
async def update_bike(
    bike_id: int,
    bike_update: BikeCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    existing = await db.get(Bike, bike_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Bike not found")
    for key, value in bike_update.model_dump().items():
        setattr(existing, key, value)
    await db.commit()
    await db.refresh(existing)
    return existing


@router.delete("/{bike_id}")
async def delete_bike(
    bike_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    bike = await db.get(Bike, bike_id)
    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")
    await db.delete(bike)
    await db.commit()
    return {"detail": "Bike deleted"}