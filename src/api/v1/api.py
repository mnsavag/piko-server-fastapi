from fastapi import APIRouter

from src.api.v1.controllers import user, contest


api_router = APIRouter()
api_router.include_router(user.router, prefix="/api/user", tags=["user"])
api_router.include_router(contest.router, prefix="/api/contest", tags=["contest"])
