from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from db.database import db, migrate
from core.config import config
from routers.users import users_bp
from routers.recipes import recipes_bp
from db.models.users import User
from db.models.recipes import Recipe

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE.get_db_url()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = config.APP.SECRET_KEY
app.config["UPLOAD_FOLDER"] = "static/uploads"

db.init_app(app)
migrate.init_app(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(recipes_bp, url_prefix="/recipes")


@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("recipes.index"))


if __name__ == "__main__":
    app.run(
        host=config.APP.HOST,
        port=config.APP.PORT,
        debug=config.APP.DEBUG,
    )
