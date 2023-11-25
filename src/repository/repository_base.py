from abc import ABC
from typing import List, TypeVar
from src.db.db import db
from sqlalchemy.sql import select


ModelType = TypeVar('ModelType')


class IRepositoryBase(ABC):
    pass


class SQLAlchemyRepository(IRepositoryBase):
    model = None

    async def get_by_id(self, id: int) -> ModelType | None:
        async with db.session_factory() as session:
            stmt = select(self.model).where(self.model.id == id)
            response = await session.execute(stmt)
            return response.scalar_one_or_none()
    
    async def get_all(self) -> List[ModelType] | None:
        async with db.session_factory() as session:
            stmt = select(self.model)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def delete_by_id(self, id) -> ModelType | None:
         async with db.session_factory() as session:
            response = await session.execute(
                select(self.model).where(self.model.id == id)
            )
            obj = response.scalar_one()
            await session.delete(obj)
            await session.commit()
            return obj

    async def update(self, obj) -> ModelType | None:
       async with db.session_factory() as session:
           session.add(obj)
           await session.commit()
           await session.refresh(obj)
           return obj
