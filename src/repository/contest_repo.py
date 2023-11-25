from typing import List
from sqlalchemy.sql import select
from src.repository.repository_base import SQLAlchemyRepository

from src.models.contest import Contest
from src.schemas.contest_schema import Option
from src.db.db import db


class ContestRepository(SQLAlchemyRepository):
    model = Contest

    async def create(self, contest: Contest) -> Contest:
        async with db.session_factory() as session:
            session.add(contest)
            await session.commit()
            await session.refresh(contest)
            return contest

    async def get_can_be_published_contests(self) -> List[Contest]:
        async with db.session_factory() as session:
            stmt = select(self.model).where(self.model.can_be_published == True)
            response = await session.execute(stmt)
            return response.scalars().all()
        
    async def get_contest_options(self, id) -> List[Option] | None:
        async with db.session_factory() as session:
            stmt = select(self.model).where(self.model.id == id)
            response = await session.execute(stmt)
            obj = response.scalar_one_or_none()
            if obj and obj.options:
                return list(obj.options)
            return None
