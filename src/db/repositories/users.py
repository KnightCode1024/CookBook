from flask_sqlalchemy import SQLAlchemy

from db.repositories.base import BaseRepository
from db.models.users import User


class UserRepository(BaseRepository):
    def __init__(self, db: SQLAlchemy):
        super().__init__(db, User)

    def get_by_email(self, email: str):
        return self.db.session.query(self.model).filter_by(email=email).first()

    def get_by_username(self, username: str):
        return self.db.session.query(self.model).first()

    def exists_by_email(self, email: str):
        return self.db.session.query(
            self.db.session.query(self.model).filter_by(email=email).exists()
        ).scalar()

    def exists_by_username(self, username: str):
        return self.db.session.query(
            self.db.session.query(self.model).filter_by(username=username).exists()
        ).scalar()

    def create_user(self, username: str, email: str, password_hash: str):
        return self.create(username=username, email=email, password_hash=password_hash)
