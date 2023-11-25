import copy
from typing import List
from fastapi import status, HTTPException, UploadFile

from src.models.contest import Contest
from src.schemas.contest_schema import ContestCreate, Option, OptionWithWinRate
from src.repository.repository_base import IRepositoryBase
from src.repository.contest_repo import ContestRepository
from src.services.category_service import CategoryService
from src.services.file_service import FileService

from src.utils.exceptions.common_exception import NotFoundException, IdNotFoundException


class ContestService:
    contest_repo: IRepositoryBase = ContestRepository()
    category_service: CategoryService = CategoryService()
    file_service: FileService = FileService()

    valid_img_formats = ["image/jpg", "image/jpeg", "image/png"]

    async def add_contest(self, contest_in: ContestCreate) -> Contest:
        categories = await self.category_service.get_all()
        all_ids = [c.id for c in categories]
        for id in contest_in.categories_ids:
            if id not in all_ids:
                raise NotFoundException(f"Category {id} doesn't exist")

        contest = Contest(
            name=contest_in.name, 
            description=contest_in.description, 
            preview_first="", 
            preview_second="", 
            categories=[c for c in categories if c.id in contest_in.categories_ids],
            options=contest_in.options
        )
        return await self.contest_repo.create(contest)
    
    async def upload_images(
            self, 
            id: int, 
            preview_first: UploadFile, 
            preview_second: UploadFile, 
            files: List[UploadFile]) -> Contest:
        
        await self.try_validate_file(preview_first)
        await self.try_validate_file(preview_second)
        for _file in files:
            await self.try_validate_file(_file)
        
        contest: Contest = await self.contest_repo.get_by_id(id)
        if not contest:
            raise IdNotFoundException(model=Contest, id=id)
        if contest.can_be_published:
            raise HTTPException(
                detail="Contest already filled", 
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        if len(contest.options) != len(files):
            raise HTTPException(
                detail="Contest and optionsFiles length are different",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        paths = await self.file_service.get_paths_to_save_contest_image(
            user_id=None,
            contest_id=id
        )

        contest.preview_first = await self.file_service.create_file(
            path_to_assets_dir=paths.root_system_path,
            path_to_server_dir=paths.preview_dir,
            _file=preview_first
        )
        contest.preview_second = await self.file_service.create_file(
            path_to_assets_dir=paths.root_system_path,
            path_to_server_dir=paths.preview_dir,
            _file=preview_second
        )
        contest.options = copy.deepcopy(contest.options)
        for i in range(len(files)):
            contest.options[i]["image"] = await self.file_service.create_file(
            path_to_assets_dir=paths.root_system_path,
            path_to_server_dir=paths.options_dir,
            _file=files[i]
        )

        contest.can_be_published = True
        return await self.contest_repo.update(contest)

    async def get_contest(self, id: int) -> Contest:
        contest: Contest = await self.contest_repo.get_by_id(id)
        if not contest:
            raise IdNotFoundException(model=Contest, id=id)
        return contest

    async def get_all_accsess_contests(self, name_filter: str | None = None) -> List[Contest]:
        contests = await self.contest_repo.get_can_be_published_contests()
        if name_filter:
            contests = list(filter(lambda contest: name_filter in contest.name, contests))
        return contests

    async def delete_contest(self, id: int) -> Contest | None:
        contest = await self.contest_repo.delete_by_id(id)
        return contest
    
    async def update_option_victory(self, id: int, option_id: int) -> List[Option]:
        contest: Contest = await self.get_contest(id)
        contest.options = copy.deepcopy(contest.options)
        
        index = [i for i, item in enumerate(contest.options) if item["id"] == option_id]
        if not index:
            raise NotFoundException(f"Option with id {option_id} not found")
        
        contest.options[index[0]]["victory_count"] += 1
        contest.count_passed = sum(item["victory_count"] for item in contest.options)

        contest = await self.contest_repo.update(contest)
        return contest.options

    async def get_options_top_list(self, id: int) -> List[OptionWithWinRate]:
        options = await self.contest_repo.get_contest_options(id)
        if not options:
            raise NotFoundException(f"Contest options not found")
        
        options.sort(key=lambda option: option["victory_count"], reverse=True)

        total_games = sum(item["victory_count"] for item in options)
        if total_games == 0:
            return list(map(
                lambda option: OptionWithWinRate(**option, win_rate=0), 
                options
            ))
        
        return list(map(
            lambda option: OptionWithWinRate(
                **option, 
                win_rate=round(option["victory_count"] / total_games * 100, 2)
            ), 
            options
        ))

    async def try_validate_file(self, _file: UploadFile):
        if _file.content_type not in self.valid_img_formats:
            raise HTTPException(
                detail=f"Available file formats is {' '.join(self.valid_img_formats)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR    
            )
