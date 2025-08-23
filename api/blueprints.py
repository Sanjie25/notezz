from flask import Blueprint, jsonify, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
import functools
from marshmallow import ValidationError, validate
from api.main import db
from api.database_models import User, Invited
from api.responses import error_response, success_response
from api.schemas import user_schema, login_schema, add_collabo

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        if not data:
            return error_response("No data found", 400)

        role = "collaborator"

        if "role" in data.keys():
            role = data["role"]
            data.pop("role")

        validated_data = login_schema.load(data)

        if User.query.filter_by(username=validated_data["username"]).first():
            return error_response("User with this username already exists", 409)

        new_user = User(username=validated_data["username"])

        new_user.set_password(validated_data["password"])
        new_user.role = role

        db.session.add(new_user)

        db.session.commit()

        login_user(new_user)

        return success_response(user_schema.dump(new_user), "User created")
    except ValidationError as err:
        return error_response(f"ValidationError: {err}", 400)
    except Exception as e:
        db.session.rollback()
        return error_response(message=f"Registration failed{e}")


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        if not data:
            return error_response("No data was found", 400)

        validated_data = login_schema.load(data)

        user = User.query.filter_by(username=validated_data["username"]).first()

        if user and user.check_password(validated_data["password"]):
            login_user(user, remember=True)
            return success_response(user_schema.dump(user), "Login Successful")

        return error_response("Incorrect password or username.", 401)

    except ValidationError as err:
        return error_response(message=err.messages)


@auth_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return success_response(None, message="Logout successful")


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
    try:
        data = request.get_json()

        if not data:
            return error_response("No data provided", 400)

        validated_data = add_collabo.load(data)

        if Invited.query.filter_by(username=validated_data["username"]).first():
            return error_response("User was already invited", 409)

        new_invite = Invited(username=validated_data["username"])

        db.session.add(new_invite)

        db.session.commit()

        return success_response(add_collabo.dump(new_invite), "User Invited", 200)
    except ValidationError as err:
        return error_response(message=err.message)
    except Exception as e:
        return error_response("Invite failed", 500)


@auth_bp.route("/check-auth", methods=["GET"])
@login_required
def check_auth():
    return success_response(
        data=user_schema.dump(current_user), message="User is authenticated"
    )


@auth_bp.route("/profile", methods=["GET"])
@login_required
def get_profile():
    return success_response(
        data=user_schema.dump(current_user), message="Profile retrieved"
    )
