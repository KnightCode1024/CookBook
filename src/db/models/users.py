import re

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, validates
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from db.models.base import BaseModel


class User(UserMixin, BaseModel):
    username: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        nullable=False,
    )
    password_hash: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
    )

    @validates("email")
    def validate_email(self, key, email):
        if not email:
            raise ValueError("Email cannot be empty")

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not re.match(pattern, email):
            raise ValueError("Invalid email format")

        return email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"{self.username}"
