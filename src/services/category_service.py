from typing import List

from src.models.category import Category
from src.repository.repository_base import IRepositoryBase
from src.repository.category_repo import CategoryRepository


class CategoryService:
    category_repo: IRepositoryBase = CategoryRepository()

    async def get_all(self) -> List[Category]:
        return await self.category_repo.get_all()
