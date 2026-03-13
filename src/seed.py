from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Bike, User
from src.app.security import get_password_hash


INITIAL_BIKES = [
    {"model": "EcoCruiser", "status": "available", "battery": 95},
    {"model": "MountainE", "status": "maintenance", "battery": 15},
    {"model": "CitySprint", "status": "rented", "battery": 60},
]

INITIAL_USERS = [
    {
        "username": "rider_one",
        "is_active": True,
        "hashed_password": get_password_hash("riderpass123"),
        "role": "rider",
    },
    {
        "username": "admin_dave",
        "is_active": True,
        "hashed_password": get_password_hash("adminpass123"),
        "role": "admin",
    },
]


async def seed_data(db: AsyncSession):
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