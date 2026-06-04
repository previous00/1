from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from datetime import date
from ..models.user import User
from ..models.student import Student
from ..models.room import Room
from ..extensions import db
from ..utils import role_required
from ..utils.responses import success, error, created

students_bp = Blueprint('students', __name__)


@students_bp.route('', methods=['GET'])
@role_required('manager', 'admin')
def list_students():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    keyword = request.args.get('keyword', '').strip()
    building_id = request.args.get('building_id', type=int)

    query = Student.query.join(User)
    if keyword:
        query = query.filter(
            (Student.student_no.contains(keyword)) |
            (User.real_name.contains(keyword))
        )
    if building_id:
        query = query.join(Room).filter(Room.building_id == building_id)

    pagination = query.order_by(Student.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return success({
        'items': [s.to_dict() for s in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
    })


@students_bp.route('/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return error('学生不存在', 404)
    return success(student.to_dict())


@students_bp.route('', methods=['POST'])
@role_required('admin')
def create_student():
    data = request.get_json()

    student_no = data.get('student_no', '').strip()
    real_name = data.get('real_name', '').strip()
    username = data.get('username', '').strip() or student_no
    password = data.get('password', '123456')

    if not student_no or not real_name:
        return error('学号和姓名为必填项')

    if Student.query.filter_by(student_no=student_no).first():
        return error('学号已存在')

    if User.query.filter_by(username=username).first():
        return error('用户名已存在')

    user = User(username=username, real_name=real_name, role='student',
                phone=data.get('phone', ''))
    user.set_password(password)
    db.session.add(user)
    db.session.flush()

    student = Student(
        user_id=user.id,
        student_no=student_no,
        gender=data.get('gender'),
        college=data.get('college'),
        major=data.get('major'),
        class_name=data.get('class_name'),
        enrollment_year=data.get('enrollment_year'),
    )
    db.session.add(student)
    db.session.commit()

    return created(student.to_dict(), '学生创建成功')


@students_bp.route('/<int:student_id>', methods=['PUT'])
@role_required('manager', 'admin')
def update_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return error('学生不存在', 404)

    data = request.get_json()
    for field in ('gender', 'college', 'major', 'class_name', 'enrollment_year'):
        if field in data:
            setattr(student, field, data[field])

    if 'real_name' in data:
        student.user.real_name = data['real_name']
    if 'phone' in data:
        student.user.phone = data['phone']

    db.session.commit()
    return success(student.to_dict(), '更新成功')


@students_bp.route('/<int:student_id>/checkin', methods=['PUT'])
@role_required('manager', 'admin')
def checkin_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return error('学生不存在', 404)

    data = request.get_json()
    room_id = data.get('room_id')
    if not room_id:
        return error('请选择房间')

    room = Room.query.get(room_id)
    if not room:
        return error('房间不存在', 404)

    if room.current_count >= room.capacity:
        return error('该房间已满')

    if student.room_id:
        old_room = Room.query.get(student.room_id)
        if old_room:
            old_room.current_count = max(0, old_room.current_count - 1)

    student.room_id = room_id
    student.check_in_date = date.today()
    student.check_out_date = None
    room.current_count += 1

    db.session.commit()
    return success(student.to_dict(), '入住成功')


@students_bp.route('/<int:student_id>/checkout', methods=['PUT'])
@role_required('manager', 'admin')
def checkout_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return error('学生不存在', 404)

    if student.room_id:
        room = Room.query.get(student.room_id)
        if room:
            room.current_count = max(0, room.current_count - 1)

    student.room_id = None
    student.check_out_date = date.today()
    db.session.commit()
    return success(student.to_dict(), '退宿成功')
