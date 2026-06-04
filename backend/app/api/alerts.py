from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from datetime import datetime
from ..models.alert import Alert
from ..extensions import db
from ..utils import role_required, get_current_user_id
from ..utils.responses import success, error

alerts_bp = Blueprint('alerts', __name__)


@alerts_bp.route('', methods=['GET'])
@role_required('manager', 'admin')
def list_alerts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    alert_type = request.args.get('alert_type')
    building_id = request.args.get('building_id', type=int)

    query = Alert.query
    if status:
        query = query.filter_by(status=status)
    if alert_type:
        query = query.filter_by(alert_type=alert_type)
    if building_id:
        query = query.filter_by(building_id=building_id)

    pagination = query.order_by(Alert.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return success({
        'items': [a.to_dict() for a in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
    })


@alerts_bp.route('/<int:alert_id>', methods=['GET'])
@role_required('manager', 'admin')
def get_alert(alert_id):
    alert = Alert.query.get(alert_id)
    if not alert:
        return error('告警不存在', 404)
    return success(alert.to_dict())


@alerts_bp.route('/<int:alert_id>/read', methods=['PUT'])
@role_required('manager', 'admin')
def mark_read(alert_id):
    alert = Alert.query.get(alert_id)
    if not alert:
        return error('告警不存在', 404)

    alert.status = 'read'
    db.session.commit()
    return success(alert.to_dict(), '已标记为已读')


@alerts_bp.route('/<int:alert_id>/resolve', methods=['PUT'])
@role_required('manager', 'admin')
def resolve_alert(alert_id):
    user_id = get_current_user_id()
    alert = Alert.query.get(alert_id)
    if not alert:
        return error('告警不存在', 404)

    alert.status = 'resolved'
    alert.handled_by = user_id
    alert.handled_at = datetime.now()
    db.session.commit()
    return success(alert.to_dict(), '已处理')


@alerts_bp.route('/unread-count', methods=['GET'])
@role_required('manager', 'admin')
def unread_count():
    count = Alert.query.filter_by(status='unread').count()
    return success({'count': count})
