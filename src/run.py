from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from db.database import db, migrate
from db.database import Base
from core.config import config
from routers.users import users_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE.get_db_url()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = config.APP.SECRET_KEY

db.init_app(app)
migrate.init_app(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'

app.register_blueprint(users_bp,  url_prefix='/users')

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

from db.models.recipe import Recipe
from db.models.users import User


if __name__ == "__main__":
    app.run(
        host=config.APP.HOST,
        port=config.APP.PORT,
        debug=config.APP.DEBUG,
    )
