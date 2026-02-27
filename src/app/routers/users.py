from typing import Any
from fastapi import APIRouter, HTTPException
from src.app.data.users_data_source import UsersDataSource
from src.app.schemas.users import UserCreate, UserResponse

router = APIRouter()
user_data_source = UsersDataSource()

@router.get("/", response_model=list[UserResponse])
def get_all_users() -> Any:
    return user_data_source.get_all_users()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int) -> Any:
    user = user_data_source.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(new_user: UserCreate) -> Any:
    user_dict = new_user.model_dump()
    user_dict["is_active"] = True
    created_user = user_data_source.create_user(user_dict)
    return created_user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserCreate) -> Any:
    updated_user = user_data_source.update_user(
        user_id, user_update.model_dump()
    )
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/{user_id}")
def delete_user(user_id: int) -> dict[str, str]:
    deleted = user_data_source.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}