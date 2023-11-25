from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase
import json


from sqlalchemy import Column


class Base(DeclarativeBase):
    __abstract__ = True


class AssociationTables():
    contest_category_id = Table(
        "contest_category_id",
        Base.metadata,
        Column("contest_id", ForeignKey("contest.id"), primary_key=True),
        Column("category_id", ForeignKey("category.id"), primary_key=True),
    )

    user_liked_contest = Table(
        "user_liked_contest",
        Base.metadata,
        Column("user_id", ForeignKey("user.id"), primary_key=True),
        Column("contest_id", ForeignKey("contest.id"), primary_key=True),
    )

    user_passed_contest = Table(
        "user_passed_contest",
        Base.metadata,
        Column("user_id", ForeignKey("user.id"), primary_key=True),
        Column("contest_id", ForeignKey("contest.id"), primary_key=True),
        
    )
