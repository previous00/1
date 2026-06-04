"""Database seed script - creates demo data."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.building import Building
from app.models.room import Room
from app.models.student import Student
from datetime import date

app = create_app()

with app.app_context():
    db.create_all()

    if User.query.first():
        print('Database already seeded.')
        sys.exit(0)

    # Create admin
    admin = User(username='admin', real_name='系统管理员', role='admin', phone='13800000001')
    admin.set_password('admin123')
    db.session.add(admin)

    # Create managers
    manager1 = User(username='manager1', real_name='王宿管', role='manager', phone='13800000002')
    manager1.set_password('123456')
    db.session.add(manager1)

    manager2 = User(username='manager2', real_name='李宿管', role='manager', phone='13800000003')
    manager2.set_password('123456')
    db.session.add(manager2)

    db.session.flush()

    # Create buildings
    b1 = Building(name='1号楼', address='校区东侧', floors=6, manager_id=manager1.id)
    b2 = Building(name='2号楼', address='校区东侧', floors=6, manager_id=manager2.id)
    b3 = Building(name='3号楼', address='校区西侧', floors=5, manager_id=manager1.id)
    db.session.add_all([b1, b2, b3])
    db.session.flush()

    # Create rooms
    rooms = []
    for building in [b1, b2, b3]:
        for floor in range(1, building.floors + 1):
            for room_num in range(1, 7):
                room_number = f'{floor}{str(room_num).zfill(2)}'
                room = Room(building_id=building.id, room_number=room_number, floor=floor, capacity=4)
                rooms.append(room)
    db.session.add_all(rooms)
    db.session.flush()

    # Create students
    students_data = [
        ('2021001', '张三', '男', '计算机学院', '软件工程', '软件2101'),
        ('2021002', '李四', '男', '计算机学院', '计算机科学', '计科2101'),
        ('2021003', '王五', '女', '信息学院', '信息安全', '信安2101'),
        ('2021004', '赵六', '男', '计算机学院', '软件工程', '软件2101'),
        ('2021005', '孙七', '女', '信息学院', '数据科学', '数科2101'),
        ('2021006', '周八', '男', '电子学院', '电子信息', '电信2101'),
        ('2021007', '吴九', '女', '计算机学院', '人工智能', '智能2101'),
        ('2021008', '郑十', '男', '电子学院', '通信工程', '通信2101'),
    ]

    available_rooms = Room.query.filter_by(building_id=b1.id).limit(4).all()
    for i, (sno, name, gender, college, major, cls) in enumerate(students_data):
        user = User(username=sno, real_name=name, role='student', phone=f'1380000{1000+i}')
        user.set_password('123456')
        db.session.add(user)
        db.session.flush()

        room = available_rooms[i % len(available_rooms)]
        student = Student(
            user_id=user.id, student_no=sno, gender=gender,
            college=college, major=major, class_name=cls,
            enrollment_year=2021, room_id=room.id, check_in_date=date(2021, 9, 1)
        )
        room.current_count += 1
        db.session.add(student)

    db.session.commit()
    print('Seed data created successfully!')
    print('Admin account: admin / admin123')
    print('Manager accounts: manager1, manager2 / 123456')
    print('Student accounts: 2021001 ~ 2021008 / 123456')
