from flask import Flask
from flask import send_from_directory
import os

def create_app():
    app = Flask(__name__, template_folder=os.path.abspath("templates"), static_folder=os.path.abspath("static"))
    app.config['UPLOAD_FOLDER'] = 'uploads'

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    from .routes import main
    app.register_blueprint(main, url_prefix="")

    return app