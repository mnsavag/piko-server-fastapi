from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, status

from src.schemas.contest_schema import (
    ContestCreate, 
    ContestOut, 
    Option, 
    OptionWithWinRate
)
from src.services.contest_service import ContestService


router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_contest(
    contest: ContestCreate,
    contest_service: ContestService = Depends(ContestService)
) -> ContestOut:
    return await contest_service.add_contest(contest)


@router.patch("/{id}/upload")
async def upload_images(
    id: int,
    preview_first: UploadFile = File(...),
    preview_second: UploadFile = File(...),
    options: List[UploadFile] = File(...),
    contest_service: ContestService = Depends(ContestService)
) -> ContestOut:
    return await contest_service.upload_images(
        id,
        preview_first, 
        preview_second, 
        options
    )


@router.get("/{id}")
async def get_contest(
    id: int, 
    contest_service: ContestService = Depends(ContestService)
) -> ContestOut:
    return await contest_service.get_contest(id)


@router.get("")
async def get_all_access_contests(
    name_filter: str | None = None,
    contest_service: ContestService = Depends(ContestService)
) -> ContestOut | List[ContestOut]:
    return await contest_service.get_all_accsess_contests(name_filter)


@router.delete("/{id}")
async def delete_contest(
    id: int,
    contest_service: ContestService = Depends(ContestService)
) -> ContestOut:
    return await contest_service.delete_contest(id)


@router.patch("/{id}/option/{option}/victory")
async def update_option_victory(
    id: int,
    option: int,
    contest_service: ContestService = Depends(ContestService)
) -> List[Option]:
    return await contest_service.update_option_victory(id, option)


@router.get("/{id}/top-list")
async def get_options_top_list(
    id: int,
    contest_service: ContestService = Depends(ContestService)
) -> List[OptionWithWinRate]:
    return await contest_service.get_options_top_list(id)
