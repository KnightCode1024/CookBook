from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, declared_attr
from sqlalchemy import Integer, func

from db.database import db


class BaseModel(db.Model):            
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True,
    )    
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )    
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), 
        onupdate=func.now(),
    )      
    
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'