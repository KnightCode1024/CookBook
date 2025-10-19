from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    current_app,
)
from flask_login import login_required, current_user

from services.recipes import RecipeService
from forms.recipes import RecipeForm

recipes_bp = Blueprint("recipes", __name__)
recipe_service = RecipeService()


@recipes_bp.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    search_query = request.args.get("search", "")

    if search_query:
        recipes_pagination = recipe_service.search_recipes(search_query, page=page)
    else:
        recipes_pagination = recipe_service.get_all_recipes_paginated(page=page)

    return render_template(
        "index.html",
        recipes=recipes_pagination.items,
        pagination=recipes_pagination,
        search_query=search_query,
    )


@recipes_bp.route("/recipe/<int:recipe_id>")
def recipe_detail(recipe_id):
    recipe = recipe_service.get_recipe_by_id(recipe_id)
    if not recipe:
        flash("Рецепт не найден", "error")
        return redirect(url_for("recipes.index"))

    return render_template("recipes/detail.html", recipe=recipe)


@recipes_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        try:
            recipe_service.create_recipe(
                title=form.title.data,
                description=form.description.data,
                ingredients=form.ingredients.data,
                instructions=form.instructions.data,
                image_file=form.image.data,
                user_id=current_user.id,
            )
            flash("Рецепт успешно добавлен!", "success")
            return redirect(url_for("recipes.index"))
        except Exception as e:
            flash("Ошибка при добавлении рецепта", "error")
            current_app.logger.error(f"Error adding recipe: {e}")

    return render_template("recipes/add.html", form=form)


@recipes_bp.route("/my-recipes")
@login_required
def my_recipes():
    page = request.args.get("page", 1, type=int)
    recipes_pagination = recipe_service.get_user_recipes(current_user.id, page=page)

    return render_template(
        "recipes/my_recipes.html",
        recipes=recipes_pagination.items,
        pagination=recipes_pagination,
    )


@recipes_bp.route("/recipe/<int:recipe_id>/delete", methods=["POST"])
@login_required
def delete_recipe(recipe_id):
    try:
        # Проверяем, принадлежит ли рецепт пользователю
        if recipe_service.can_user_delete_recipe(recipe_id, current_user.id):
            recipe_service.delete_recipe(recipe_id, current_user.id)
            flash("Рецепт успешно удален", "success")
        else:
            flash("Вы не можете удалить этот рецепт", "error")
    except Exception as e:
        current_app.logger.error(f"Error deleting recipe: {str(e)}")
        flash("Ошибка при удалении рецепта", "error")

    return redirect(url_for("recipes.my_recipes"))
