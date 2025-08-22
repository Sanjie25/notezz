from app.main import ma
from marshmallow import fields, validate, pre_load, post_load
from app.database_models import Note, User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

    id = ma.auto_field(dump_only=True)
    username = ma.auto_field(required=True, validate=validate.Length(min=3, max=80))
    password = fields.Str(
        required=True, load_only=True, validate=validate.Length(min=6)
    )
    role = ma.auto_field(validate=validate.OneOf(["admin", "collaborator"]))
    created_at = ma.auto_field(dump_only=True)

    @pre_load
    def process_password(self, data, **kwargs):
        if "password" in data:
            data["password"] = data["password"].strip()
        return data


class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Note
        load_instance = True

    id = ma.auto_field(dump_only=True)
    title = ma.auto_field(required=True, validate=validate.Length(min=1, max=200))
    body = ma.auto_field(required=True)
    author_id = ma.auto_field(dump_only=True)
    created_at = ma.auto_field(dump_only=True)
    updated_at = ma.auto_field(dump_only=True)
    # tags = fields.List(fields.Str(), required=False)
    author = fields.Nested(UserSchema, only=("id", "username"), dump_only=True)


note_schema = NoteSchema()
user_schema = UserSchema()
users_schema = UserSchema(many=True)
notes_schema = NoteSchema(many=True)
