from fastapi import FastAPI
from src.app.routers import bikes, users, rentals


app = FastAPI(title="EcoMute Bike Sharing API")

app.include_router(bikes.router, prefix="/bikes", tags=["bikes"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(rentals.router, prefix="/rentals", tags=["rentals"])