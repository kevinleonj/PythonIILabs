from typing import Any
from fastapi import APIRouter
from src.app.schemas.rentals import RentalProcessing

router = APIRouter()

@router.post("/", status_code = 201)
def process_rental(rental: RentalProcessing) -> Any:
    return {
        "message": "Rental processed successfuly",
        "bike_id": rental.bike_id,
        "user_id": rental.user_id,
        "battery_level": rental.battery_level,
    }