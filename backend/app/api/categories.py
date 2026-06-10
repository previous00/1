from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Category, User

categories_bp = Blueprint('categories', __name__)


@categories_bp.route('', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories])


@categories_bp.route('', methods=['POST'])
@jwt_required()
def create_category():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != 'admin':
        return jsonify({'message': '权限不足'}), 403

    data = request.get_json()
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'message': '分类名称不能为空'}), 400

    if Category.query.filter_by(name=name).first():
        return jsonify({'message': '分类已存在'}), 400

    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict()), 201


@categories_bp.route('/<int:category_id>', methods=['PUT'])
@jwt_required()
def update_category(category_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != 'admin':
        return jsonify({'message': '权限不足'}), 403

    category = Category.query.get_or_404(category_id)
    data = request.get_json()
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'message': '分类名称不能为空'}), 400

    existing = Category.query.filter_by(name=name).first()
    if existing and existing.id != category_id:
        return jsonify({'message': '分类已存在'}), 400

    category.name = name
    db.session.commit()
    return jsonify(category.to_dict())


@categories_bp.route('/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != 'admin':
        return jsonify({'message': '权限不足'}), 403

    category = Category.query.get_or_404(category_id)
    if category.books:
        return jsonify({'message': '该分类下还有图书，无法删除'}), 400

    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': '删除成功'})
