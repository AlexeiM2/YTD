# app/__init__.py
from flask import Flask
from flask_cors import CORS

def create_app():
    # Crear la aplicación Flask
    app = Flask(__name__, static_folder='../frontend', static_url_path='')
    CORS(app)

    # Importar y registrar las rutas desde routes.py
    from .routes import app_bp  # Importa el Blueprint
    app.register_blueprint(app_bp)  # Registra el Blueprint

    return app