# routes/users.py
from http import HTTPStatus as status
from flask_login import login_user, logout_user, login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, flash, request
from urllib.parse import urlparse, urljoin

from services.users import UserService
from forms.users import LoginForm, RegisterForm

users_bp = Blueprint("users", __name__)

user_service = UserService()


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = user_service.authenticate_user(
            email=form.email.data, password=form.password.data
        )

        if user:
            login_user(user)
            flash("Вы успешно вошли!", "success")

            next_page = request.args.get("next")
            if next_page and is_safe_url(next_page):
                return redirect(next_page)
            return redirect(url_for("index"))
        else:
            flash("Неверный email или пароль", "error")

    return render_template("users/login.html", form=form)


@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegisterForm()
    if form.validate_on_submit():
        user, message = user_service.register_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        if user:
            flash("Регистрация прошла успешно! Теперь вы можете войти.", "success")
            return redirect(url_for("users.login"))
        else:
            flash(message, "error")

    return render_template("users/register.html", form=form)


@users_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из системы", "success")
    return redirect(url_for("index"))
