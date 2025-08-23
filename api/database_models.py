from datetime import datetime
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash
from api.main import db

__all__ = ["User", "Note", "Tag"]


class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    tags = db.relationship(
        "Tag", secondary="note_tags", back_populates="notes", lazy="dynamic"
    )

    def to_dict(self):
        author = db.session.execute(
            db.select(User).filter_by(id=self.author_id)
        ).fetchone()
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "author_id": self.author_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "author": author[0].username if author else None,
        }

    def __repr__(self):
        return f"<Note {self.title}>"


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Relationships
    notes = db.relationship(
        "Note", secondary="note_tags", back_populates="tags", lazy="dynamic"
    )

    def __repr__(self):
        return f"<Tag {self.name}>"


class Note_Tags(db.Model):
    __tablename__ = "note_tags"

    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(
        db.Integer, db.ForeignKey("notes.id"), nullable=False, index=True
    )
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.now)


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(2048), nullable=False)
    role = db.Column(db.Enum("admin", "collaborator"), default="collaborator")
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    created_notes = db.relationship(
        "Note", backref="author", lazy=True, cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "created_at": self.created_at.isoformat(),
        }

    def set_password(self, password):
        self.password_hash = generate_password_hash(
            password, method="pbkdf2:sha256", salt_length=4
        )

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"<User {self.username}>"


class Invited(db.Model):
    __tablename__ = "invited"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "created_at": self.created_at,
        }
