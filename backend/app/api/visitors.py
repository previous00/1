from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from datetime import datetime
from ..models.visitor import Visitor
from ..models.user import User
from ..extensions import db
from ..utils import role_required, get_current_user_id
from ..utils.responses import success, error, created

visitors_bp = Blueprint('visitors', __name__)


@visitors_bp.route('', methods=['POST'])
@jwt_required()
def create_visitor():
    user_id = get_current_user_id()
    data = request.get_json()

    name = data.get('name', '').strip()
    if not name:
        return error('访客姓名为必填项')

    visitor = Visitor(
        name=name,
        id_card=data.get('id_card', ''),
        phone=data.get('phone', ''),
        reason=data.get('reason', ''),
        visit_target_id=data.get('visit_target_id'),
        building_id=data.get('building_id'),
        applicant_id=user_id,
        visit_start=datetime.fromisoformat(data['visit_start']) if data.get('visit_start') else None,
        visit_end=datetime.fromisoformat(data['visit_end']) if data.get('visit_end') else None,
    )
    db.session.add(visitor)
    db.session.commit()
    return created(visitor.to_dict(), '访客申请已提交')


@visitors_bp.route('', methods=['GET'])
@role_required('manager', 'admin')
def list_visitors():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    building_id = request.args.get('building_id', type=int)

    query = Visitor.query
    if status:
        query = query.filter_by(status=status)
    if building_id:
        query = query.filter_by(building_id=building_id)

    pagination = query.order_by(Visitor.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return success({
        'items': [v.to_dict() for v in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
    })


@visitors_bp.route('/my', methods=['GET'])
@jwt_required()
def my_visitors():
    user_id = get_current_user_id()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    pagination = Visitor.query.filter_by(applicant_id=user_id).order_by(
        Visitor.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)

    return success({
        'items': [v.to_dict() for v in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
    })


@visitors_bp.route('/<int:visitor_id>', methods=['GET'])
@jwt_required()
def get_visitor(visitor_id):
    visitor = Visitor.query.get(visitor_id)
    if not visitor:
        return error('访客记录不存在', 404)
    return success(visitor.to_dict())


@visitors_bp.route('/<int:visitor_id>/approve', methods=['PUT'])
@role_required('manager', 'admin')
def approve_visitor(visitor_id):
    user_id = get_current_user_id()
    visitor = Visitor.query.get(visitor_id)
    if not visitor:
        return error('访客记录不存在', 404)

    if visitor.status != 'pending':
        return error('该申请已处理')

    visitor.status = 'approved'
    visitor.approved_by = user_id
    db.session.commit()
    return success(visitor.to_dict(), '已批准')


@visitors_bp.route('/<int:visitor_id>/reject', methods=['PUT'])
@role_required('manager', 'admin')
def reject_visitor(visitor_id):
    user_id = get_current_user_id()
    visitor = Visitor.query.get(visitor_id)
    if not visitor:
        return error('访客记录不存在', 404)

    if visitor.status != 'pending':
        return error('该申请已处理')

    visitor.status = 'rejected'
    visitor.approved_by = user_id
    db.session.commit()
    return success(visitor.to_dict(), '已拒绝')


@visitors_bp.route('/<int:visitor_id>/complete', methods=['PUT'])
@role_required('manager', 'admin')
def complete_visitor(visitor_id):
    visitor = Visitor.query.get(visitor_id)
    if not visitor:
        return error('访客记录不存在', 404)

    visitor.status = 'completed'
    visitor.actual_leave = datetime.now()
    db.session.commit()
    return success(visitor.to_dict(), '访问已结束')
