from pydantic import BaseModel, Field


class TripInput(BaseModel):
    distance_km: float = Field(gt=0, le=100)
    battery_level: float = Field(ge=0, le=100)