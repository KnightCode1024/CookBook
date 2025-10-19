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

    def update_recipe(self, recipe_id, user_id, **kwargs):
        recipe = (
            self.db.session.query(self.model)
            .filter_by(id=recipe_id, user_id=user_id)
            .first()
        )

        if recipe:
            for key, value in kwargs.items():
                if value is not None:
                    setattr(recipe, key, value)
            self.db.session.commit()
            return recipe
        return None

    def update_recipe_with_image(self, recipe_id, user_id, image_file=None, **kwargs):
        recipe = (
            self.db.session.query(self.model)
            .filter_by(id=recipe_id, user_id=user_id)
            .first()
        )

        if not recipe:
            return None

        if image_file and image_file.filename:
            import os
            from werkzeug.utils import secure_filename

            if recipe.image_filename:
                old_image_path = os.path.join(
                    "static", "uploads", recipe.image_filename
                )
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

            filename = secure_filename(image_file.filename)
            image_filename = f"{user_id}_{filename}"
            upload_path = os.path.join("static", "uploads", image_filename)
            image_file.save(upload_path)
            kwargs["image_filename"] = image_filename

        for key, value in kwargs.items():
            if value is not None and key != "image_file":
                setattr(recipe, key, value)

        self.db.session.commit()
        return recipe
