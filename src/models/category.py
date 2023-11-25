from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, List

from src.models.base import Base, AssociationTables


if TYPE_CHECKING:
    from src.models.contest import Contest


class Category(Base):
    __tablename__= "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))

    contests: Mapped[List["Contest"]] = relationship(
        secondary=AssociationTables.contest_category_id, back_populates="categories"
    )
