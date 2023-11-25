from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import String, DateTime, JSON, ForeignKey
from datetime import datetime
from typing import TYPE_CHECKING, List

from src.models.base import Base, AssociationTables
from src.schemas.contest_schema import OptionCreate, Option


if TYPE_CHECKING:
    from src.models.user import User
    from src.models.category import Category

    
class Contest(Base):
    __tablename__= "contest"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(250))
    preview_first: Mapped[str] = mapped_column(nullable=True)
    preview_second: Mapped[str] = mapped_column(nullable=True)

    options: Mapped[List] = mapped_column(JSON)
    amount_options: Mapped[int]

    count_passed: Mapped[int] = mapped_column(default=0)
    can_be_published: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    user: Mapped["User"] = relationship(back_populates="contests")

    categories: Mapped[List["Category"]] = relationship(
        secondary=AssociationTables.contest_category_id, back_populates="contests",
    )
    users_liked: Mapped[List["User"]] = relationship(
        secondary=AssociationTables.user_liked_contest, back_populates="contests_liked"
    )
    users_passed: Mapped[List["User"]] = relationship(
        secondary=AssociationTables.user_passed_contest, back_populates="contests_passed"
    )

    def __init__(
            self, 
            name: str, 
            description: str, 
            categories: List["Category"], 
            preview_first: str, 
            preview_second: str, 
            options: List[OptionCreate]
        ):
        self.amount_options = len(options)
        self.options = []
        for i in range(1, self.amount_options + 1):
            self.options.append(Option(id=i, name=options[i - 1].name).model_dump())

        self.name = name
        self.description = description
        self.categories = categories
        self.preview_first = preview_first
        self.preview_second = preview_second
