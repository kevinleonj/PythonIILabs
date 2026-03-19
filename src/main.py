from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.app.routers import bikes, users, rentals, admin, auth, stations, predictions
from src.database import engine, async_session
from src.models import Base
from src.seed import seed_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        await seed_data(session)

    yield

    await engine.dispose()


app = FastAPI(title="EcoMute Bike Sharing API", lifespan=lifespan)

app.include_router(bikes.router, prefix="/bikes", tags=["bikes"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(rentals.router, prefix="/rentals", tags=["rentals"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(auth.router, tags=["auth"])
app.include_router(stations.router, prefix="/stations", tags=["stations"])
app.include_router(predictions.router, prefix="/predict", tags=["predictions"])