from typing import Optional, Literal
from pydantic import BaseModel, Field

class BikeBase(BaseModel):
    model: str
    battery: float = Field(ge=0, le=100)
    status: Literal["available", "rented", "maintenance"]
    station_id: Optional[int] = None

class BikeCreate(BikeBase):
    pass

class BikeResponse(BikeBase):
    id: int
