from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, declared_attr
from sqlalchemy import Integer, func

from db.database import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    created_at = db.Column(
        db.DateTime,
        server_default=func.now(),
    )
    updated_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"
