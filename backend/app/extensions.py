from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()
migrate = Migrate()


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify(code=401, message='Token已过期，请重新登录'), 401


@jwt.invalid_token_loader
def invalid_token_callback(error_string):
    return jsonify(code=422, message=f'无效的Token: {error_string}'), 422


@jwt.unauthorized_loader
def missing_token_callback(error_string):
    return jsonify(code=401, message='缺少Authorization头，请先登录'), 401


@jwt.token_verification_failed_loader
def token_verification_failed_callback(jwt_header, jwt_payload):
    return jsonify(code=422, message='Token验证失败'), 422
