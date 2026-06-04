from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from ..models.access_log import AccessLog
from ..models.user import User
from ..extensions import db
from ..utils import role_required, get_current_user_id
from ..utils.responses import success, error

access_bp = Blueprint('access', __name__)


@access_bp.route('/logs', methods=['GET'])
@role_required('manager', 'admin')
def list_logs():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    building_id = request.args.get('building_id', type=int)
    direction = request.args.get('direction')
    is_authorized = request.args.get('is_authorized')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    keyword = request.args.get('keyword', '').strip()

    query = AccessLog.query

    if building_id:
        query = query.filter_by(building_id=building_id)
    if direction:
        query = query.filter_by(direction=direction)
    if is_authorized is not None:
        query = query.filter_by(is_authorized=is_authorized == 'true')
    if start_date:
        query = query.filter(AccessLog.created_at >= start_date)
    if end_date:
        query = query.filter(AccessLog.created_at <= end_date + ' 23:59:59')
    if keyword:
        query = query.join(User).filter(User.real_name.contains(keyword))

    pagination = query.order_by(AccessLog.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return success({
        'items': [l.to_dict() for l in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
    })


@access_bp.route('/logs/my', methods=['GET'])
@jwt_required()
def my_logs():
    user_id = get_current_user_id()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    pagination = AccessLog.query.filter_by(user_id=user_id).order_by(
        AccessLog.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)

    return success({
        'items': [l.to_dict() for l in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
    })


@access_bp.route('/logs/<int:log_id>', methods=['GET'])
@role_required('manager', 'admin')
def get_log(log_id):
    log = AccessLog.query.get(log_id)
    if not log:
        return error('记录不存在', 404)
    return success(log.to_dict())


@access_bp.route('/manual', methods=['POST'])
@role_required('manager')
def manual_entry():
    data = request.get_json()
    user_id = data.get('user_id')
    building_id = data.get('building_id')
    direction = data.get('direction', 'in')

    if not building_id:
        return error('请选择楼栋')

    log = AccessLog(
        user_id=user_id,
        building_id=building_id,
        direction=direction,
        method='manual',
        is_authorized=True,
    )
    db.session.add(log)
    db.session.commit()
    return success(log.to_dict(), '手动登记成功')
