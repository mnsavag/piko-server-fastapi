from pydantic import BaseModel, Field, field_validator
from typing import List
from datetime import datetime

from src.utils.alias_generators import to_camel


class OptionCreate(BaseModel):
    name: str = Field(min_length=1, max_length=25)

class Option(BaseModel):
    id: int
    name: str
    image: str = ""
    victory_count: int = 0

class OptionWithWinRate(Option):
    win_rate: float


class ContestCreate(BaseModel):
    name: str = Field(min_length=1, max_length=25)
    description: str = Field(min_length=1, max_length=250)
    categories_ids: List[int] = Field(min_length=1, max_length=2)
    options: List[OptionCreate]

    class Config:
        alias_generator = to_camel

    @field_validator("options")
    @classmethod
    def available_len(cls, value: List) -> str:
        if len(value) not in [8, 16, 32, 64]:
            raise ValueError('Available options len [8, 16, 32, 64]')
        return value

class ContestOut(BaseModel):
    id: int
    name: str
    description: str
    preview_first: str
    preview_second: str
    amount_options: int
    can_be_published: bool
    user_id: int | None = None
    options: List[Option]
    count_passed: int
    created_at: datetime
