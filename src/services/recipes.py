import os

from werkzeug.utils import secure_filename
from db.repositories.recipes import RecipeRepository

from db.database import db


class RecipeService:
    def __init__(self):
        self.recipe_repo = RecipeRepository(db)

    def get_all_recipes_paginated(self, page=1):
        return self.recipe_repo.get_paginated(page=page)

    def get_recipe_by_id(self, recipe_id):
        return self.recipe_repo.get_by_id(recipe_id)

    def get_user_recipes(self, user_id, page=1):
        return self.recipe_repo.get_by_user_id(user_id, page=page)

    def search_recipes(self, query, page=1):
        return self.recipe_repo.search_recipes(query, page=page)

    def create_recipe(
        self, title, description, ingredients, instructions, image_file, user_id
    ):
        try:
            image_filename = None
            if image_file and image_file.filename:
                upload_dir = "static/uploads"

                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir, exist_ok=True)

                filename = secure_filename(image_file.filename)
                if not filename:
                    raise ValueError("Invalid filename")

                image_filename = f"{user_id}_{filename}"
                upload_path = os.path.join(upload_dir, image_filename)

                image_file.save(upload_path)

                if not os.path.exists(upload_path):
                    raise ValueError("Failed to save image file")

            recipe = self.recipe_repo.create_recipe(
                title=title,
                description=description,
                ingredients=ingredients,
                instructions=instructions,
                image_filename=image_filename,
                user_id=user_id,
            )

            return recipe

        except Exception as e:
            db.session.rollback()
            raise e

    def delete_recipe(self, recipe_id, user_id):
        try:
            return self.recipe_repo.delete_recipe(recipe_id, user_id)
        except Exception as e:
            db.session.rollback()
            raise e

    def can_user_delete_recipe(self, recipe_id, user_id):
        return self.recipe_repo.user_owns_recipe(recipe_id, user_id)

    def update_recipe(
        self,
        recipe_id,
        user_id,
        title=None,
        description=None,
        ingredients=None,
        instructions=None,
        image_file=None,
    ):
        try:
            update_data = {
                "title": title,
                "description": description,
                "ingredients": ingredients,
                "instructions": instructions,
            }

            update_data = {k: v for k, v in update_data.items() if v is not None}

            if image_file == "remove":
                import os

                recipe = self.recipe_repo.get_by_id(recipe_id)
                if recipe and recipe.image_filename:
                    old_image_path = os.path.join(
                        "static", "uploads", recipe.image_filename
                    )
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                    update_data["image_filename"] = None
                return self.recipe_repo.update_recipe(recipe_id, user_id, **update_data)

            elif image_file:
                return self.recipe_repo.update_recipe_with_image(
                    recipe_id, user_id, image_file, **update_data
                )
            else:
                return self.recipe_repo.update_recipe(recipe_id, user_id, **update_data)

        except Exception as e:
            db.session.rollback()
            raise e

    def can_user_edit_recipe(self, recipe_id, user_id):
        return self.recipe_repo.user_owns_recipe(recipe_id, user_id)

    def get_recipe_for_edit(self, recipe_id, user_id):
        recipe = self.recipe_repo.get_by_id(recipe_id)
        if recipe and recipe.user_id == user_id:
            return recipe
        return None
