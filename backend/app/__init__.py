import os
from flask import Flask
from .config import Config
from .extensions import db, jwt, cors, migrate


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    migrate.init_app(app, db)

    from .api import auth_bp, users_bp, students_bp, buildings_bp, rooms_bp
    from .api import faces_bp, access_bp, visitors_bp, alerts_bp, statistics_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(students_bp, url_prefix='/api/students')
    app.register_blueprint(buildings_bp, url_prefix='/api/buildings')
    app.register_blueprint(rooms_bp, url_prefix='/api/rooms')
    app.register_blueprint(faces_bp, url_prefix='/api/faces')
    app.register_blueprint(access_bp, url_prefix='/api/access')
    app.register_blueprint(visitors_bp, url_prefix='/api/visitors')
    app.register_blueprint(alerts_bp, url_prefix='/api/alerts')
    app.register_blueprint(statistics_bp, url_prefix='/api/statistics')

    from .errors.handlers import register_error_handlers
    register_error_handlers(app)

    with app.app_context():
        db.create_all()

    return app
