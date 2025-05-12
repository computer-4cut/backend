from flask import Flask
import os
from app.config import config_by_name


def create_app(config_name='dev'):
    app = Flask(__name__)

    app.config.from_object(config_by_name[config_name])

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    from app.api.routes import api_bp
    app.register_blueprint(api_bp)

    return app