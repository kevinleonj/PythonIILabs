from pydantic import BaseModel


class StationCreate(BaseModel):
    name: str
    location: str
    capacity: int


class StationResponse(BaseModel):
    id: int
    name: str
    location: str
    capacity: int