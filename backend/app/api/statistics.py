from flask import Blueprint, request
from datetime import datetime, timedelta
from sqlalchemy import func, cast, Date
from ..models.access_log import AccessLog
from ..models.alert import Alert
from ..models.student import Student
from ..models.building import Building
from ..models.room import Room
from ..models.user import User
from ..extensions import db
from ..utils import role_required
from ..utils.responses import success

statistics_bp = Blueprint('statistics', __name__)


@statistics_bp.route('/overview', methods=['GET'])
@role_required('manager', 'admin')
def overview():
    today = datetime.now().date()
    total_students = Student.query.count()
    total_buildings = Building.query.count()
    total_rooms = Room.query.count()
    today_access = AccessLog.query.filter(
        cast(AccessLog.created_at, Date) == today
    ).count()
    unread_alerts = Alert.query.filter_by(status='unread').count()

    return success({
        'total_students': total_students,
        'total_buildings': total_buildings,
        'total_rooms': total_rooms,
        'today_access': today_access,
        'unread_alerts': unread_alerts,
    })


@statistics_bp.route('/access-trend', methods=['GET'])
@role_required('manager', 'admin')
def access_trend():
    days = request.args.get('days', 7, type=int)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days - 1)

    results = db.session.query(
        cast(AccessLog.created_at, Date).label('date'),
        func.count(AccessLog.id).label('count')
    ).filter(
        cast(AccessLog.created_at, Date) >= start_date
    ).group_by(
        cast(AccessLog.created_at, Date)
    ).order_by('date').all()

    date_counts = {r.date.isoformat(): r.count for r in results}
    trend = []
    current = start_date
    while current <= end_date:
        trend.append({
            'date': current.isoformat(),
            'count': date_counts.get(current.isoformat(), 0)
        })
        current += timedelta(days=1)

    return success(trend)


@statistics_bp.route('/building-rank', methods=['GET'])
@role_required('manager', 'admin')
def building_rank():
    results = db.session.query(
        Building.name,
        func.count(AccessLog.id).label('count')
    ).join(AccessLog, Building.id == AccessLog.building_id).group_by(
        Building.name
    ).order_by(func.count(AccessLog.id).desc()).limit(10).all()

    return success([{'name': r.name, 'count': r.count} for r in results])


@statistics_bp.route('/hourly', methods=['GET'])
@role_required('manager', 'admin')
def hourly_distribution():
    today = datetime.now().date()
    results = db.session.query(
        func.strftime('%H', AccessLog.created_at).label('hour'),
        func.count(AccessLog.id).label('count')
    ).filter(
        cast(AccessLog.created_at, Date) == today
    ).group_by('hour').order_by('hour').all()

    hours = {str(i).zfill(2): 0 for i in range(24)}
    for r in results:
        hours[r.hour] = r.count

    return success([{'hour': h, 'count': c} for h, c in hours.items()])


@statistics_bp.route('/alerts-summary', methods=['GET'])
@role_required('manager', 'admin')
def alerts_summary():
    results = db.session.query(
        Alert.alert_type,
        func.count(Alert.id).label('count')
    ).group_by(Alert.alert_type).all()

    return success([{'type': r.alert_type, 'count': r.count} for r in results])
