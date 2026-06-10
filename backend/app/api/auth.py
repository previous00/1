from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return jsonify({'message': '用户名和密码不能为空'}), 400

    if len(password) < 6:
        return jsonify({'message': '密码长度不能少于6位'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': '用户名已存在'}), 400

    user = User(username=username, role='reader')
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': '注册成功'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'message': '用户名或密码错误'}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({
        'token': token,
        'user': user.to_dict()
    })


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    return jsonify(user.to_dict())
