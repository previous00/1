from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from ..models.user import User
from ..extensions import db
from ..utils import get_current_user_id
from ..utils.responses import success, error, created

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return error('请求数据为空')

    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    real_name = data.get('real_name', '').strip()
    phone = data.get('phone', '').strip()
    role = data.get('role', 'student')

    if not username or not password or not real_name:
        return error('用户名、密码和姓名为必填项')

    if len(password) < 6:
        return error('密码长度不能少于6位')

    if role not in ('student', 'manager', 'admin'):
        return error('无效的角色类型')

    if User.query.filter_by(username=username).first():
        return error('用户名已存在')

    user = User(username=username, real_name=real_name, phone=phone, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return created(user.to_dict(), '注册成功')


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return error('请求数据为空')

    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return error('用户名和密码不能为空')

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return error('用户名或密码错误', 401)

    if not user.is_active:
        return error('账号已被禁用', 403)

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return success({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }, '登录成功')


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    return success({'access_token': access_token})


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_current_user_id()
    user = User.query.get(user_id)
    if not user:
        return error('用户不存在', 404)
    return success(user.to_dict())


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_current_user_id()
    user = User.query.get(user_id)
    if not user:
        return error('用户不存在', 404)

    data = request.get_json()
    if data.get('real_name'):
        user.real_name = data['real_name'].strip()
    if data.get('phone'):
        user.phone = data['phone'].strip()

    db.session.commit()
    return success(user.to_dict(), '更新成功')


@auth_bp.route('/password', methods=['PUT'])
@jwt_required()
def change_password():
    user_id = get_current_user_id()
    user = User.query.get(user_id)

    data = request.get_json()
    old_password = data.get('old_password', '')
    new_password = data.get('new_password', '')

    if not user.check_password(old_password):
        return error('原密码错误')

    if len(new_password) < 6:
        return error('新密码长度不能少于6位')

    user.set_password(new_password)
    db.session.commit()
    return success(message='密码修改成功')
