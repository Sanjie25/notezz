from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        os.environ.get("SQLALCHEMY_DATABASE_URI")
        or "mysql+pymysql://super_user:password@localhost/notezz"
    )
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or "super-secret-key"
    # app.config.from_object("config.py")

    db.init_app(app)
    login_manager.init_app(app)
    ma.init_app(app)

    with app.app_context():
        db.create_all()

    # configuring the login manager
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.session_protection = "strong"

    from api.database_models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # @app.route("/")
    # def index():
    #     return "index"

    from api.blueprints import auth_bp

    app.register_blueprint(auth_bp)

    from api.notes import notes_bp

    app.register_blueprint(notes_bp)
    return app
