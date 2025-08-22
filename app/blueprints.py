from flask import Blueprint, request, flash, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.main import db
from app.database_models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET"])
def register():
    return render_template("register.html")


@auth_bp.route("/register/<role>", methods=["GET", "POST"])
def register_roles(role):
    if request.method == "POST":
        print(1)
        username = request.form["username"]
        password = request.form["password"]
        error = None

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        elif role not in ["collaborator", "admin"]:
            error = "Note correct role"

        print(2)
        if User.query.filter_by(username=username).first():
            error = f"User {username} is already registered as {role}."

        print(3)
        if error is None:
            print(4)
            new_user = User(username=username, role=role)
            new_user.set_password(password)

            print(5)
            db.session.add(new_user)
            db.session.commit()

            print(6)
            login_user(new_user)
            print(7)

            return redirect(url_for("notes.index"))

        flash(error)
    return render_template(f"register_{role}.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        print(4)

        if user and user.check_password(password):
            print(5)
            login_user(user, remember=True)

            print(current_user.username)
            return redirect(url_for("notes.index"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
