from typing import Any, Annotated
from fastapi import APIRouter, Depends
from src.app.schemas.rentals import RentalProcessing
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import get_db
from src.models import Rental
from src.app.logger import logger

router = APIRouter()

DatabaseSession = Annotated[AsyncSession, Depends(get_db)]


@router.post("/", status_code=201)
async def process_rental(rental: RentalProcessing, db: DatabaseSession) -> Any:
    logger.info(f"Processing rental for bike {rental.bike_id} by user {rental.user_id}")
    new_rental = Rental(
        bike_id=rental.bike_id,
        user_id=rental.user_id,
        battery_level=rental.battery_level,
    )
    db.add(new_rental)
    await db.commit()
    await db.refresh(new_rental)
    logger.info(f"Rental saved with id: {new_rental.id}")
    return {
        "message": "Rental processed and saved successfully",
        "id": new_rental.id,
        "bike_id": new_rental.bike_id,
        "user_id": new_rental.user_id,
        "battery_level": new_rental.battery_level,
    }


@router.get("/")
async def get_all_rentals(db: DatabaseSession) -> Any:
    logger.info("Fetching all rentals")
    statement = select(Rental)
    result = await db.execute(statement)
    all_rentals = result.scalars().all()
    if not all_rentals:
        logger.warning("No rentals found")
    return [
        {
            "id": rental.id,
            "bike_id": rental.bike_id,
            "user_id": rental.user_id,
            "battery_level": rental.battery_level,
        }
        for rental in all_rentals
    ]