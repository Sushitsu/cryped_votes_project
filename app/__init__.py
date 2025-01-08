from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Charge la configuration
    db.init_app(app)  # Initialise SQLAlchemy avec l'application
    return app
