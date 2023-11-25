from fastapi import APIRouter, Depends, status
from pydantic import type_adapter

from src.schemas.user_schema import UserCreate, UserOut
from src.services.user_service import UserService


router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    user_service: UserService = Depends(UserService)
) -> UserOut:
    user = await user_service.add_user(user)
    userOut = UserOut(
        id=user.id,
        username=user.username,
        email=user.email,
        created_at=user.created_at
    )
    return userOut


@router.get("/{id}")
async def get_user(
    id: int,
    user_service: UserService = Depends(UserService)
) -> UserOut:
    user = await user_service.get_user_by_id(id)
    userOut = UserOut(
        id=user.id,
        username=user.username,
        email=user.email,
        created_at=user.created_at
    )
    return userOut
