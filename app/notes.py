from flask import Blueprint, jsonify, request, flash, render_template, redirect, url_for
from app.main import db
from flask_login import current_user, login_required
from app.database_models import Note, User, Tag
from app.blueprints import admin_required
from app.schemas import note_schema

notes_bp = Blueprint("notes", __name__)


@notes_bp.route("/notes", methods=["POST", "GET"])
@login_required
def create_note():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        tags = request.form["tags"].split()
        error = None

        if not title:
            error = "title is required"
        elif not content:
            error = "content is required"

        if error is None:
            new_note = Note(title=title, body=content, author_id=current_user.id)

            db.session.add(new_note)

            for tag in tags:
                new_tag = Tag(name=tag)

            db.session.commit()

            return redirect(url_for("notes.index"))

    return render_template("create_note.html")


@notes_bp.route("/notes/<int:note_id>", methods=["POST", "GET"])
@login_required
def get_note(note_id):
    note = Note.query.get_or_404(note_id)
    author = db.session.execute(db.select(User).filter_by(id=note.author_id)).fetchone()

    return render_template("note_view.html", note=note, author=author)


@notes_bp.route("/notes_json/<int:note_id>", methods=["GET"])
def get_notejson(note_id):
    note = Note.query.get_or_404(note_id)

    # return jsonify(note.to_dict())
    return note_schema.dump(note)


@notes_bp.route("/delete/<int:note_id>")
@login_required
@admin_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)

    db.session.delete(note)
    db.session.commit()

    return redirect(url_for("notes.index"))


@notes_bp.route("/notes")
@login_required
def notes_view():
    return redirect(url_for("notes.index"))


@notes_bp.route("/", methods=["GET"])
@login_required
def index():
    notes = db.session.execute(db.select(Note).order_by(Note.title)).fetchall()
    size = len(notes)

    return render_template("index.html", notes=notes, size=size)


@notes_bp.route("/notes/<int:note_id>/edit", methods=["POST", "GET"])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        tags = request.form["tags"]
        error = None

        if not title:
            error = "title is required"
        elif not content:
            error = "content is required"

        if error is None:
            note.title = title
            note.body = content

            for tag in tags:
                new_tag = Tag(name=tag)

            db.session.commit()

            return redirect(url_for("notes.index"))

    return render_template("edit_note.html", note=note)
