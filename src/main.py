from fastapi import FastAPI
from src.app.routers import bikes, users, rentals, admin
from contextlib import asynccontextmanager
from src.database import engine
from src.models import Base

app = FastAPI(title="EcoMute Bike Sharing API")

app.include_router(bikes.router, prefix="/bikes", tags=["bikes"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(rentals.router, prefix="/rentals", tags=["rentals"])
app.include_router(admin.router, prefix="/admin",tags=["admin"])

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(title="EcoMute Bike Sharing API", lifespan=lifespan)
