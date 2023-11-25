from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import DateTime

from datetime import datetime
from typing import List, TYPE_CHECKING

from src.models.base import Base, AssociationTables
from src.utils.validators import isValidEmail


if TYPE_CHECKING:
    from src.models.contest import Contest


class User(Base):
    __tablename__= "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    contests: Mapped[List["Contest"]] = relationship(back_populates="user")
    contests_liked: Mapped[List["Contest"]] = relationship(
        secondary=AssociationTables.user_liked_contest, back_populates="users_liked"
    )
    contests_passed: Mapped[List["Contest"]] = relationship(
        secondary=AssociationTables.user_passed_contest, back_populates="users_passed"
    )

    
    @validates("email")
    def validate_email(self, key, email):
        if not isValidEmail(email):
            raise ValueError("failed simplified email validation")
        return email
