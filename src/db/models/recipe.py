from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import BaseModel


class Recipe(BaseModel):
    title: Mapped[str] = mapped_column(String(50))
    discription: Mapped[str] = mapped_column(String(500))
    cook_time: Mapped[int] = mapped_column(Integer())
