from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import BorrowRecord, Book, User
from datetime import datetime

borrows_bp = Blueprint('borrows', __name__)


@borrows_bp.route('', methods=['GET'])
@jwt_required()
def get_borrows():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    if user.role == 'admin':
        query = BorrowRecord.query
    else:
        query = BorrowRecord.query.filter_by(user_id=user_id)

    query = query.order_by(BorrowRecord.borrow_date.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'records': [r.to_dict() for r in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    })


@borrows_bp.route('', methods=['POST'])
@jwt_required()
def borrow_book():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    book_id = data.get('book_id')

    if not book_id:
        return jsonify({'message': '请选择要借阅的图书'}), 400

    book = Book.query.get_or_404(book_id)
    if book.available_count <= 0:
        return jsonify({'message': '该图书已无可借阅库存'}), 400

    existing = BorrowRecord.query.filter_by(
        user_id=user_id, book_id=book_id, status='borrowed'
    ).first()
    if existing:
        return jsonify({'message': '您已借阅此书且尚未归还'}), 400

    record = BorrowRecord(user_id=user_id, book_id=book_id)
    book.available_count -= 1
    db.session.add(record)
    db.session.commit()

    return jsonify(record.to_dict()), 201


@borrows_bp.route('/<int:record_id>/return', methods=['POST'])
@jwt_required()
def return_book(record_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != 'admin':
        return jsonify({'message': '只有管理员可以处理归还'}), 403

    record = BorrowRecord.query.get_or_404(record_id)
    if record.status == 'returned':
        return jsonify({'message': '该记录已归还'}), 400

    record.status = 'returned'
    record.return_date = datetime.utcnow()
    record.book.available_count += 1
    db.session.commit()

    return jsonify(record.to_dict())
