from flask import Blueprint, request
from api.main import db
from flask_login import current_user, login_required
from api.database_models import Note
from api.blueprints import admin_required
from api.responses import error_response, success_response
from api.schemas import note_schema

notes_bp = Blueprint("notes", __name__, url_prefix="/notes")


@notes_bp.route("/create", methods=["POST"])
@login_required
def create_note():
    try:
        data = request.get_json()
        if not data:
            return error_response("No data provided", 400)

        new_note = Note(
            title=data["title"],
            body=data["body"],
            author_id=current_user.id,
        )

        db.session.add(new_note)
        db.session.commit()

        return success_response(data=note_schema.dump(new_note), status_code=201)
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to create note: {e}", 400)


@notes_bp.route("/<int:note_id>", methods=["GET"])
def get_note(note_id):
    note = Note.query.get_or_404(note_id)

    return success_response(data=note_schema.dump(note), status_code=200)


@notes_bp.route("/all", methods=["GET"])
def get_all_note():
    notes = db.session.execute(db.select(Note)).fetchall()
    result = {}
    n = 0

    for note in notes:
        result[n] = note_schema.dump(note[0])
        n += 1

    return success_response(data=result, status_code=200)


@notes_bp.route("/delete_by_title", methods=["DELETE"])
@login_required
@admin_required
def delete_note_by_name():
    try:
        data = request.get_json()
        if not data:
            return error_response("No data provided", 400)

        note = db.session.execute(
            db.select(Note).filter_by(title=data["title"])
        ).fetchone()

        db.session.delete(note[0])
        db.session.commit()

        return success_response(None, "")

    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to delete note: {e}", 500)


@notes_bp.route("/<int:note_id>/delete", methods=["DELETE"])
@login_required
@admin_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)

    db.session.delete(note)
    db.session.commit()

    return success_response(None, "")


@notes_bp.route("/<int:note_id>/edit", methods=["PUT"])
@login_required
def edit_note(note_id):
    try:
        note = Note.query.get_or_404(note_id)

        data = request.get_json()
        if not data:
            return error_response("No data provided", 400)

        if "title" in data:
            note.title = data["title"]
        if "body" in data:
            note.body = data["body"]

        db.session.commit()

        return success_response(data=note_schema.dump(note))

    except Exception as e:
        db.session.rollback()
        return error_response("Failed to edit note", status_code=304)
