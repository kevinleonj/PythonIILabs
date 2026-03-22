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


@router.post("/")
def predict_trip_duration(trip_data: TripInput) -> Any:
    logger.info(f"Prediction requested: distance={trip_data.distance_km}, battery={trip_data.battery_level}")
    input_data = pandas.DataFrame(
        [[trip_data.distance_km, trip_data.battery_level]],
        columns=["distance_km", "battery_level"],
    )

    prediction = model.predict(input_data)
    estimated_minutes = round(float(prediction[0]), 2)

    logger.info(f"Prediction result: {estimated_minutes} minutes")
    return {"estimated_minutes": estimated_minutes}