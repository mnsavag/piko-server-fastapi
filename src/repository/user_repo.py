from sqlalchemy.sql import select
from src.repository.repository_base import SQLAlchemyRepository

from src.models.user import User
from src.db.db import db
from src.schemas.user_schema import UserCreate


class UserRepository(SQLAlchemyRepository):
    model = User

    async def create(self, obj_in: UserCreate) -> User:
        async with db.session_factory() as session:
            db_obj = User(**obj_in.model_dump())
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    async def get_by_id(self, id: int) -> User | None:
        async with db.session_factory() as session:
            stmt = select(User).where(User.id == id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one_or_none()

    async def get_by_mail(self, email: str) -> User | None:
        async with db.session_factory() as session:
            stmt = select(User).where(User.email == email)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one_or_none()
