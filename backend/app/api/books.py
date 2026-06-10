from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Book, User

books_bp = Blueprint('books', __name__)


@books_bp.route('', methods=['GET'])
def get_books():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    keyword = request.args.get('keyword', '').strip()
    category_id = request.args.get('category_id', type=int)

    query = Book.query
    if keyword:
        query = query.filter(
            db.or_(
                Book.title.contains(keyword),
                Book.author.contains(keyword),
                Book.isbn.contains(keyword)
            )
        )
    if category_id:
        query = query.filter_by(category_id=category_id)

    query = query.order_by(Book.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'books': [b.to_dict() for b in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    })


@books_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict())


@books_bp.route('', methods=['POST'])
@jwt_required()
def create_book():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != 'admin':
        return jsonify({'message': '权限不足'}), 403

    data = request.get_json()
    if not data.get('title') or not data.get('author'):
        return jsonify({'message': '书名和作者不能为空'}), 400

    book = Book(
        title=data['title'],
        author=data['author'],
        isbn=data.get('isbn'),
        publisher=data.get('publisher'),
        publish_date=data.get('publish_date'),
        description=data.get('description'),
        category_id=data.get('category_id'),
        total_count=data.get('total_count', 1),
        available_count=data.get('total_count', 1)
    )
    db.session.add(book)
    db.session.commit()

    return jsonify(book.to_dict()), 201


@books_bp.route('/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != 'admin':
        return jsonify({'message': '权限不足'}), 403

    book = Book.query.get_or_404(book_id)
    data = request.get_json()

    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.isbn = data.get('isbn', book.isbn)
    book.publisher = data.get('publisher', book.publisher)
    book.publish_date = data.get('publish_date', book.publish_date)
    book.description = data.get('description', book.description)
    book.category_id = data.get('category_id', book.category_id)

    new_total = data.get('total_count')
    if new_total is not None:
        diff = new_total - book.total_count
        book.total_count = new_total
        book.available_count = max(0, book.available_count + diff)

    db.session.commit()
    return jsonify(book.to_dict())


@books_bp.route('/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != 'admin':
        return jsonify({'message': '权限不足'}), 403

    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': '删除成功'})
