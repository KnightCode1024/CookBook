from typing import Type, TypeVar

from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model

T = TypeVar("T", bound=Model)

class BaseRepository:
    def __init__(self,db: SQLAlchemy ,model: Type[T]):
        self.db = db
        self.model = model

    def get_by_id(self, id: int):
        return self.db.session.get(self.model, id)

    def get_all(self):
        return self.db.session.query(self.model).all()
    
    def create(self, **kwargs):
        isinstance = self.model(**kwargs)
        self.db.session.add(instance)
        self.db.session.commit()
        return isinstance

    def update(self, id: int, **kwargs):
        isinstance = self.get_by_id(id)
        if isinstance:
            for key, value in kwargs.items():
                setattr(isinstance, key, value)
            self.db.session.commit()
            return True
        return False

    def delete(self, id: int):
        isinstance = self.get_by_id(id)
        if isinstance:
            self.db.session.delete(isinstance)
            self.db.session.commit()
            return True
        return False