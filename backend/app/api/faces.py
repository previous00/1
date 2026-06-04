import os
import time
from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from ..models.face import FaceEncoding
from ..models.user import User
from ..models.access_log import AccessLog
from ..models.alert import Alert
from ..models.student import Student
from ..models.room import Room
from ..extensions import db
from ..services.face_service import enroll_face, verify_face
from ..utils import role_required, get_current_user_id
from ..utils.responses import success, error, created

faces_bp = Blueprint('faces', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@faces_bp.route('/enroll', methods=['POST'])
@jwt_required()
def enroll():
    user_id = get_current_user_id()

    if 'file' not in request.files:
        return error('请上传人脸图片')

    file = request.files['file']
    if file.filename == '':
        return error('未选择文件')

    if not allowed_file(file.filename):
        return error('仅支持 PNG/JPG 格式图片')

    filename = f"{user_id}_{int(time.time())}.jpg"
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    face_record, err = enroll_face(user_id, filepath)
    if err:
        os.remove(filepath)
        return error(err)

    return created(face_record.to_dict(), '人脸录入成功')


@faces_bp.route('/my', methods=['GET'])
@jwt_required()
def my_faces():
    user_id = get_current_user_id()
    faces = FaceEncoding.query.filter_by(user_id=user_id).order_by(FaceEncoding.created_at.desc()).all()
    return success([f.to_dict() for f in faces])


@faces_bp.route('/<int:face_id>', methods=['DELETE'])
@jwt_required()
def delete_face(face_id):
    user_id = get_current_user_id()
    user = User.query.get(user_id)

    face = FaceEncoding.query.get(face_id)
    if not face:
        return error('记录不存在', 404)

    if face.user_id != user_id and user.role != 'admin':
        return error('权限不足', 403)

    if os.path.exists(face.image_path):
        os.remove(face.image_path)

    db.session.delete(face)
    db.session.commit()

    from ..services.face_service import invalidate_cache
    invalidate_cache()

    return success(message='删除成功')


@faces_bp.route('/verify', methods=['POST'])
@jwt_required()
def verify():
    if 'file' not in request.files:
        return error('请上传人脸图片')

    file = request.files['file']
    if not allowed_file(file.filename):
        return error('仅支持 PNG/JPG 格式图片')

    filename = f"verify_{int(time.time())}.jpg"
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    matched_user_id, confidence, err = verify_face(filepath)
    os.remove(filepath)

    if err:
        return success({'matched': False, 'confidence': confidence, 'message': err})

    user = User.query.get(matched_user_id)
    return success({
        'matched': True,
        'confidence': confidence,
        'user': user.to_dict() if user else None,
    })


@faces_bp.route('/access', methods=['POST'])
@jwt_required()
def face_access():
    building_id = request.form.get('building_id', type=int)
    direction = request.form.get('direction', 'in')

    if not building_id:
        return error('请选择楼栋')

    if 'file' not in request.files:
        return error('请上传人脸图片')

    file = request.files['file']
    if not allowed_file(file.filename):
        return error('仅支持 PNG/JPG 格式图片')

    filename = f"access_{int(time.time())}.jpg"
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    matched_user_id, confidence, err = verify_face(filepath)

    is_authorized = False
    user = None

    if matched_user_id:
        user = User.query.get(matched_user_id)
        if user:
            if user.role == 'admin':
                is_authorized = True
            elif user.role == 'manager':
                from ..models.building import Building
                building = Building.query.get(building_id)
                is_authorized = building and building.manager_id == user.id
            else:
                student = Student.query.filter_by(user_id=user.id).first()
                if student and student.room_id:
                    room = Room.query.get(student.room_id)
                    is_authorized = room and room.building_id == building_id

    log = AccessLog(
        user_id=matched_user_id,
        building_id=building_id,
        direction=direction,
        method='face',
        confidence=confidence,
        is_authorized=is_authorized,
        snapshot_path=filepath,
    )
    db.session.add(log)
    db.session.flush()

    if not is_authorized:
        alert_type = 'unknown_face' if not matched_user_id else 'unauthorized'
        description = '未识别人员尝试进入' if not matched_user_id else f'{user.real_name} 尝试进入非授权楼栋'
        alert = Alert(
            access_log_id=log.id,
            building_id=building_id,
            alert_type=alert_type,
            description=description,
            snapshot_path=filepath,
        )
        db.session.add(alert)

    db.session.commit()

    return success({
        'authorized': is_authorized,
        'user_name': user.real_name if user else None,
        'confidence': confidence,
        'direction': direction,
        'message': '通行成功' if is_authorized else ('身份未识别，禁止通行' if not matched_user_id else '非授权楼栋，禁止通行'),
    })
