from db.database import db
from db.models.base import BaseModel
from flask_login import current_user


class Recipe(BaseModel):
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(300), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", backref=db.backref("recipes", lazy=True))

    def __repr__(self):
        return f"{self.title}"
