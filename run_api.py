import os
from app.main import create_app, db

if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db.create_all()

    port = int(os.environ.get("PORT", 12345))
    host = os.environ.get("HOST", "127.0.0.1")
    app.run(debug=True, host=host, port=port)
