from typing import Any, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models import User
from src.app.security import verify_password, create_access_token
from src.app.logger import logger

router = APIRouter()


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Any:
    logger.info(f"Login attempt for username: {form_data.username}")
    statement = select(User).where(User.username == form_data.username)
    result = await db.execute(statement)
    user = result.scalar_one_or_none()

    if user is None:
        logger.warning(f"Login failed: user not found: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    password_is_correct = verify_password(
        form_data.password, user.hashed_password
    )

    if not password_is_correct:
        logger.warning(f"Login failed: wrong password for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}
    )

    logger.info(f"Login successful for user: {form_data.username}")
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }