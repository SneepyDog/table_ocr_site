from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)


## === app/__init__.py ===
from flask import Flask
from flask import send_from_directory
import os

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'uploads'

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    from .routes import main
    app.register_blueprint(main)

    return app