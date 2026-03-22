from typing import Any
from fastapi import APIRouter, HTTPException
from src.app.data.users_data_source import UsersDataSource
from src.app.schemas.users import UserCreate, UserResponse
from src.app.logger import logger

router = APIRouter()
user_data_source = UsersDataSource()


@router.get("/", response_model=list[UserResponse])
def get_all_users() -> Any:
    logger.info("Fetching all users")
    users = user_data_source.get_all_users()
    if not users:
        logger.warning("No users found")
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int) -> Any:
    logger.info(f"Fetching user with id: {user_id}")
    user = user_data_source.get_user(user_id)
    if user is None:
        logger.warning(f"User not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(new_user: UserCreate) -> Any:
    logger.info(f"Creating new user: {new_user.username}")
    user_dict = new_user.model_dump()
    user_dict["is_active"] = True
    created_user = user_data_source.create_user(user_dict)
    return created_user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserCreate) -> Any:
    logger.info(f"Updating user: {user_id}")
    updated_user = user_data_source.update_user(
        user_id, user_update.model_dump()
    )
    if updated_user is None:
        logger.warning(f"User not found for update: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/{user_id}")
def delete_user(user_id: int) -> dict[str, str]:
    logger.info(f"Deleting user: {user_id}")
    deleted = user_data_source.delete_user(user_id)
    if not deleted:
        logger.warning(f"User not found for deletion: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}