from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import BaseModel

class User(BaseModel):
    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
    )
    email: Mapped[str]