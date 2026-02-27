from typing import Any, Optional, Literal
from fastapi import APIRouter, HTTPException, Depends
from src.app.data.bikes_data_source import BikesDataSource
from src.app.data.bikes_data_source import get_bike_datasource
from src.app.schemas.bikes import BikeCreate, BikeResponse
router = APIRouter()



@router.get("/", response_model=list[BikeResponse])
def get_all_bikes(
    status: Optional[Literal["available", "rented", "maintenance"]] = None, 
    datasource: BikesDataSource = Depends(get_bike_datasource),
) -> Any:
    all_bikes = datasource.get_all_bikes()
    if status is not None:
        filtered_bikes = [
            bike for bike in all_bikes if bike["status"] == status
        ]
        return filtered_bikes
    return all_bikes

@router.get("/{bike_id}", response_model = BikeResponse)
def get_bike(bike_id: int,
             datasource: BikesDataSource = Depends(get_bike_datasource)) -> Any:
    bike = datasource.get_bike(bike_id)
    if bike is None:
        raise HTTPException(status_code=404, detail = "Bike not found")
    return bike

@router.post("/", response_model=BikeResponse, status_code=201)
def create_bike(new_bike: BikeCreate,
                datasource: BikesDataSource = Depends(get_bike_datasource)) -> Any:
    created_bike = datasource.create_bike(new_bike.model_dump())
    return created_bike

@router.put("/{bike_id}", response_model=BikeResponse)
def update_bike(bike_id:int, bike_update:BikeCreate,
                datasource: BikesDataSource = Depends(get_bike_datasource)) -> Any:
    updated_bike = datasource.update_bike(
        bike_id, bike_update.model_dump()
    )
    if updated_bike is None:
        raise HTTPException(status_code=404, detail= "Bike not found")
    return updated_bike

@router.delete("/{bike_id}")
def delete_bike(bike_id: int, datasource: BikesDataSource = Depends(get_bike_datasource)) -> dict[str, str]:
    deleted = datasource.delete_bike(bike_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bike not found")
    return {"detail": "Bike deleted"}