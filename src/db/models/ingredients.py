from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import BaseModel


class Ingredients(db.Model):
    name: Mapped[str] = mapped_column(String(50))
