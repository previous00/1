from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
        os.path.abspath(os.path.dirname(__file__)), '..', 'library.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'library-management-secret-key-2024'
    app.config['JSON_AS_ASCII'] = False

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    from app.api.auth import auth_bp
    from app.api.books import books_bp
    from app.api.categories import categories_bp
    from app.api.borrows import borrows_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(books_bp, url_prefix='/api/books')
    app.register_blueprint(categories_bp, url_prefix='/api/categories')
    app.register_blueprint(borrows_bp, url_prefix='/api/borrows')

    with app.app_context():
        db.create_all()
        _init_admin(app)

    return app


def _init_admin(app):
    from app.models import User
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
