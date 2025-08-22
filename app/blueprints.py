from flask import Blueprint, request, flash, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
import functools
from app.main import db
from app.database_models import User, Invited

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET"])
def register():
    return render_template("register.html")


@auth_bp.route("/register/<role>", methods=["GET", "POST"])
def register_roles(role):
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        elif role not in ["collaborator", "admin"]:
            error = "Note correct role"

        if User.query.filter_by(username=username).first():
            error = f"User {username} is already registered as {role}."

        if (
            role == "collaborator"
            and not Invited.query.filter_by(username=username).first()
        ):
            error = f"User {username} is not an invited collaborator."

        if error is None:
            new_user = User(username=username, role=role)
            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            return redirect(url_for("notes.index"))

        flash(error)
    return render_template(f"register_{role}.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=True)

            return redirect(url_for("notes.index"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if current_user.role != "admin":
            flash("Admin priviledges required")
            return redirect(url_for("notes.index"))

        return view(**kwargs)

    return wrapped_view


@auth_bp.route("/add_collab", methods=["GET", "POST"])
@admin_required
def add_collaborator():
    if request.method == "POST":
        username = request.form["username"]
        error = None

        if not username:
            error = "collaborator name required to invite."

        if error == None:
            new_invite = Invited(username=username)

            db.session.add(new_invite)
            db.session.commit()

            return redirect(url_for("auth.register_roles", role="collaborator"))

        flash(error)
    return render_template("invite.html")
