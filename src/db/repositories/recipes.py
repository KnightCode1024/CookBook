from flask_sqlalchemy import SQLAlchemy

from db.repositories.base import BaseRepository
from db.models.recipes import Recipe


class RecipeRepository(BaseRepository):
    def __init__(self, db: SQLAlchemy):
        super().__init__(db, Recipe)

    def get_paginated(self, page=1, per_page=6):
        return self.model.query.order_by(self.model.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    def get_by_user_id(self, user_id, page=1, per_page=6):
        return (
            self.model.query.filter_by(user_id=user_id)
            .order_by(self.model.created_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )

    def search_recipes(self, query, page=1, per_page=6):
        return (
            self.model.query.filter(
                self.model.title.ilike(f"%{query}%")
                | self.model.description.ilike(f"%{query}%")
                | self.model.ingredients.ilike(f"%{query}%")
            )
            .order_by(self.model.created_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )

    def create_recipe(
        self, title, description, ingredients, instructions, image_filename, user_id
    ):
        return self.create(
            title=title,
            description=description,
            ingredients=ingredients,
            instructions=instructions,
            image_filename=image_filename,
            user_id=user_id,
        )

    def delete_recipe(self, recipe_id, user_id):
        recipe = (
            self.db.session.query(self.model)
            .filter_by(id=recipe_id, user_id=user_id)
            .first()
        )

        if recipe:
            if recipe.image_filename:
                import os

                image_path = os.path.join("static", "uploads", recipe.image_filename)
                if os.path.exists(image_path):
                    os.remove(image_path)

            self.db.session.delete(recipe)
            self.db.session.commit()
            return True
        return False

    def user_owns_recipe(self, recipe_id, user_id):
        return self.db.session.query(
            self.model.query.filter_by(id=recipe_id, user_id=user_id).exists()
        ).scalar()
