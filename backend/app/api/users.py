from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from ..models.user import User
from ..extensions import db
from ..utils import role_required
from ..utils.responses import success, error

users_bp = Blueprint('users', __name__)


@users_bp.route('', methods=['GET'])
@role_required('admin')
def list_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    role = request.args.get('role')
    keyword = request.args.get('keyword', '').strip()

    query = User.query
    if role:
        query = query.filter_by(role=role)
    if keyword:
        query = query.filter(
            (User.username.contains(keyword)) | (User.real_name.contains(keyword))
        )

    pagination = query.order_by(User.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return success({
        'items': [u.to_dict() for u in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
    })


@users_bp.route('/<int:user_id>', methods=['GET'])
@role_required('admin')
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return error('用户不存在', 404)
    return success(user.to_dict())


@users_bp.route('/<int:user_id>', methods=['PUT'])
@role_required('admin')
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return error('用户不存在', 404)

    data = request.get_json()
    if data.get('real_name'):
        user.real_name = data['real_name']
    if data.get('phone'):
        user.phone = data['phone']
    if data.get('role') and data['role'] in ('student', 'manager', 'admin'):
        user.role = data['role']

    db.session.commit()
    return success(user.to_dict(), '更新成功')


@users_bp.route('/<int:user_id>/status', methods=['PUT'])
@role_required('admin')
def toggle_user_status(user_id):
    user = User.query.get(user_id)
    if not user:
        return error('用户不存在', 404)

    data = request.get_json()
    user.is_active = data.get('is_active', not user.is_active)
    db.session.commit()
    return success(user.to_dict(), '状态更新成功')


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@role_required('admin')
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return error('用户不存在', 404)

    db.session.delete(user)
    db.session.commit()
    return success(message='删除成功')
