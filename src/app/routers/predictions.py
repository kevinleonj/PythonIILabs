import asyncio
import os
from typing import Any

import pandas
import joblib
from fastapi import APIRouter

from src.app.schemas.predictions import TripInput
from src.app.logger import logger

router = APIRouter()

model_file_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "ml",
    "trip_predictor.joblib",
)
model_file_path = os.path.normpath(model_file_path)

model = joblib.load(model_file_path)


def _run_prediction(distance_km: float, battery_level: float) -> float:
    input_data = pandas.DataFrame(
        [[distance_km, battery_level]],
        columns=["distance_km", "battery_level"],
    )
    return float(model.predict(input_data)[0])


@router.post("/")
async def predict_trip_duration(trip_data: TripInput) -> Any:
    logger.info(
        "Prediction requested: distance=%s, battery=%s",
        trip_data.distance_km,
        trip_data.battery_level,
    )
    estimated_minutes = await asyncio.to_thread(
        _run_prediction,
        trip_data.distance_km,
        trip_data.battery_level,
    )
    estimated_minutes = round(estimated_minutes, 2)
    logger.info("Prediction result: %s minutes", estimated_minutes)
    return {"estimated_minutes": estimated_minutes}