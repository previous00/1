from flask import Blueprint, request
from ..models.room import Room
from ..models.building import Building
from ..extensions import db
from ..utils import role_required
from ..utils.responses import success, error, created

rooms_bp = Blueprint('rooms', __name__)


@rooms_bp.route('', methods=['GET'])
@role_required('student', 'manager', 'admin')
def list_rooms():
    building_id = request.args.get('building_id', type=int)
    floor = request.args.get('floor', type=int)

    query = Room.query
    if building_id:
        query = query.filter_by(building_id=building_id)
    if floor:
        query = query.filter_by(floor=floor)

    rooms = query.order_by(Room.building_id, Room.room_number).all()
    return success([r.to_dict() for r in rooms])


@rooms_bp.route('/<int:room_id>', methods=['GET'])
@role_required('student', 'manager', 'admin')
def get_room(room_id):
    room = Room.query.get(room_id)
    if not room:
        return error('房间不存在', 404)
    return success(room.to_dict())


@rooms_bp.route('', methods=['POST'])
@role_required('admin')
def create_room():
    data = request.get_json()
    building_id = data.get('building_id')
    room_number = data.get('room_number', '').strip()

    if not building_id or not room_number:
        return error('楼栋和房间号为必填项')

    if not Building.query.get(building_id):
        return error('楼栋不存在', 404)

    existing = Room.query.filter_by(building_id=building_id, room_number=room_number).first()
    if existing:
        return error('该房间号已存在')

    room = Room(
        building_id=building_id,
        room_number=room_number,
        floor=data.get('floor'),
        capacity=data.get('capacity', 4),
    )
    db.session.add(room)
    db.session.commit()
    return created(room.to_dict(), '房间创建成功')


@rooms_bp.route('/<int:room_id>', methods=['PUT'])
@role_required('admin')
def update_room(room_id):
    room = Room.query.get(room_id)
    if not room:
        return error('房间不存在', 404)

    data = request.get_json()
    if 'capacity' in data:
        room.capacity = data['capacity']
    if 'floor' in data:
        room.floor = data['floor']

    db.session.commit()
    return success(room.to_dict(), '更新成功')


@rooms_bp.route('/<int:room_id>', methods=['DELETE'])
@role_required('admin')
def delete_room(room_id):
    room = Room.query.get(room_id)
    if not room:
        return error('房间不存在', 404)

    if room.current_count > 0:
        return error('房间内还有学生，无法删除')

    db.session.delete(room)
    db.session.commit()
    return success(message='删除成功')


@rooms_bp.route('/<int:room_id>/students', methods=['GET'])
@role_required('manager', 'admin')
def list_room_students(room_id):
    room = Room.query.get(room_id)
    if not room:
        return error('房间不存在', 404)

    return success([s.to_dict() for s in room.students])
