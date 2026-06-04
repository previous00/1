from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask import jsonify
from ..models.user import User


def get_current_user_id():
    """Get current user ID as int from JWT identity (stored as string)."""
    identity = get_jwt_identity()
    return int(identity)


def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_current_user_id()
            user = User.query.get(user_id)
            if not user or not user.is_active:
                return jsonify(code=401, message='用户不存在或已禁用'), 401
            if user.role not in roles:
                return jsonify(code=403, message='权限不足'), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
