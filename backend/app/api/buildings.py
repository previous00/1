from flask import Blueprint, request
from ..models.building import Building
from ..extensions import db
from ..utils import role_required
from ..utils.responses import success, error, created

buildings_bp = Blueprint('buildings', __name__)


@buildings_bp.route('', methods=['GET'])
@role_required('student', 'manager', 'admin')
def list_buildings():
    buildings = Building.query.order_by(Building.name).all()
    return success([b.to_dict() for b in buildings])


@buildings_bp.route('/<int:building_id>', methods=['GET'])
@role_required('student', 'manager', 'admin')
def get_building(building_id):
    building = Building.query.get(building_id)
    if not building:
        return error('楼栋不存在', 404)
    return success(building.to_dict())


@buildings_bp.route('', methods=['POST'])
@role_required('admin')
def create_building():
    data = request.get_json()
    name = data.get('name', '').strip()
    if not name:
        return error('楼栋名称为必填项')

    if Building.query.filter_by(name=name).first():
        return error('楼栋名称已存在')

    building = Building(
        name=name,
        address=data.get('address', ''),
        floors=data.get('floors'),
        manager_id=data.get('manager_id'),
    )
    db.session.add(building)
    db.session.commit()
    return created(building.to_dict(), '楼栋创建成功')


@buildings_bp.route('/<int:building_id>', methods=['PUT'])
@role_required('admin')
def update_building(building_id):
    building = Building.query.get(building_id)
    if not building:
        return error('楼栋不存在', 404)

    data = request.get_json()
    if 'name' in data:
        building.name = data['name']
    if 'address' in data:
        building.address = data['address']
    if 'floors' in data:
        building.floors = data['floors']
    if 'manager_id' in data:
        building.manager_id = data['manager_id']

    db.session.commit()
    return success(building.to_dict(), '更新成功')


@buildings_bp.route('/<int:building_id>', methods=['DELETE'])
@role_required('admin')
def delete_building(building_id):
    building = Building.query.get(building_id)
    if not building:
        return error('楼栋不存在', 404)

    db.session.delete(building)
    db.session.commit()
    return success(message='删除成功')


@buildings_bp.route('/<int:building_id>/rooms', methods=['GET'])
@role_required('student', 'manager', 'admin')
def list_building_rooms(building_id):
    building = Building.query.get(building_id)
    if not building:
        return error('楼栋不存在', 404)

    rooms = building.rooms
    return success([r.to_dict() for r in rooms])
