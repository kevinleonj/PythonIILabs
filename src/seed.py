from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Bike
from src.models import User


INITIAL_BIKES = [
    {"model": "EcoCruiser", "status": "available", "battery": 95},
    {"model": "MountainE", "status": "maintenance", "battery": 15},
    {"model": "CitySprint", "status": "rented", "battery": 60},
]

INITIAL_USERS = [
    {"username": "rider_one", "is_active": True},
    {"username": "admin_dave", "is_active": True},
]


async def seed_data(db: AsyncSession):
    """
    Checks if the DB is empty. If yes, populates it with mock data.
    This runs once at startup inside the lifespan function.
    """
    print("Checking if database needs seeding...")

    result = await db.execute(select(Bike).limit(1))
    first_bike = result.scalar_one_or_none()

    if first_bike:
        print("Database already contains data. Skipping seed.")
        return

    print("Seeding database with initial mock data...")

    for bike_data in INITIAL_BIKES:
        new_bike = Bike(**bike_data)
        db.add(new_bike)

    for user_data in INITIAL_USERS:
        new_user = User(**user_data)
        db.add(new_user)


    await db.commit()
    print("Seeding complete!")