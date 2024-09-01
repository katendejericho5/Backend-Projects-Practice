# app/utils.py
from flask import Flask
from config import Config
from app.extensions import db, jwt, bcrypt, limiter
from app.todos import bp as todos_bp
from app.auth import bp as auth_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    limiter.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(todos_bp)

    return app
