from src.repository.repository_base import SQLAlchemyRepository
from src.models.category import Category


class CategoryRepository(SQLAlchemyRepository):
    model = Category
