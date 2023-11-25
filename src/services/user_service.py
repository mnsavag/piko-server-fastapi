from src.models.user import User
from src.repository.repository_base import IRepositoryBase
from src.repository.user_repo import UserRepository

from src.schemas.user_schema import UserCreate
from src.utils.exceptions.common_exception import AlreadyExistException


class UserService:
    user_repo: IRepositoryBase = UserRepository()

    async def add_user(self, user: UserCreate) -> User:
        await self.is_unique_user(user.email)        
        user = await self.user_repo.create(user)
        return user
    
    async def get_user_by_id(self, id: int) -> User:
        user = await self.user_repo.get_by_id(id)
        return user
    
    async def is_unique_user(self, email: str) -> bool:
        if await self.user_repo.get_by_mail(email):
            raise AlreadyExistException(User, "email", email)
        return True
