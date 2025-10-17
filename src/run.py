from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from db.database import db, migrate
from db.database import Base
from core.config import config

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE.get_db_url()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate.init_app(app, db)


from db.models.recipe import Recipe
from db.models.users import User


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/recipe/add/")
def add_recipe():
    return render_template("recipes/add_recipe.html")


if __name__ == "__main__":
    app.run(
        host=config.APP.HOST,
        port=config.APP.PORT,
        debug=config.APP.DEBUG,
    )

