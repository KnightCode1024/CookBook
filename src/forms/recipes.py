from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class RecipeForm(FlaskForm):
    title = StringField(
        "Название блюда",
        validators=[
            DataRequired(message="Название обязательно"),
            Length(min=2, max=200, message="Название должно быть от 2 до 200 символов"),
        ],
    )
    description = TextAreaField(
        "Описание",
        validators=[
            Length(max=500, message="Описание не должно превышать 500 символов")
        ],
    )
    ingredients = TextAreaField(
        "Ингредиенты",
        validators=[
            DataRequired(message="Ингредиенты обязательны"),
            Length(min=10, message="Слишком короткий список ингредиентов"),
        ],
    )
    instructions = TextAreaField(
        "Рецепт",
        validators=[
            DataRequired(message="Рецепт обязателен"),
            Length(min=20, message="Слишком короткий рецепт"),
        ],
    )
    image = FileField(
        "Фото блюда",
        validators=[FileAllowed(["jpg", "jpeg", "png", "gif"], "Только изображения!")],
    )
    submit = SubmitField("Добавить рецепт")
