# app/__init__.py
from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__, static_folder='../frontend', static_url_path='')
    CORS(app)

    # Importar y registrar las rutas
    from .routes import app as routes_blueprint
    app.register_blueprint(routes_blueprint)

    return app