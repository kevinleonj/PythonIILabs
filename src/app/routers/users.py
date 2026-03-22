from typing import Any
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import get_db
from src.models import User
from src.app.schemas.users import UserCreate, UserResponse
from src.app.logger import logger

router = APIRouter()


@router.get("/", response_model=list[UserResponse])
async def get_all_users(
    db: AsyncSession = Depends(get_db),
) -> Any:
    logger.info("Fetching all users")
    result = await db.execute(select(User))
    users = result.scalars().all()
    if not users:
        logger.warning("No users found")
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    logger.info("Fetching user with id: %d", user_id)
    user = await db.get(User, user_id)
    if user is None:
        logger.warning("User not found: %d", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    new_user: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    logger.info("Creating new user: %s", new_user.username)
    user_dict = new_user.model_dump()
    user_dict["is_active"] = True
    user_dict["hashed_password"] = "placeholder"
    user_dict["role"] = "rider"
    created_user = User(**user_dict)
    db.add(created_user)
    await db.commit()
    await db.refresh(created_user)
    return created_user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    logger.info("Updating user: %d", user_id)
    existing = await db.get(User, user_id)
    if existing is None:
        logger.warning("User not found for update: %d", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user_update.model_dump().items():
        setattr(existing, key, value)
    await db.commit()
    await db.refresh(existing)
    return existing


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    logger.info("Deleting user: %d", user_id)
    user = await db.get(User, user_id)
    if not user:
        logger.warning("User not found for deletion: %d", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return {"detail": "User deleted"}