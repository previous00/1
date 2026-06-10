from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='reader')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'created_at': self.created_at.isoformat()
        }


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    books = db.relationship('Book', backref='category', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'book_count': len(self.books)
        }


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True)
    publisher = db.Column(db.String(100))
    publish_date = db.Column(db.String(20))
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    total_count = db.Column(db.Integer, default=1)
    available_count = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'publisher': self.publisher,
            'publish_date': self.publish_date,
            'description': self.description,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'total_count': self.total_count,
            'available_count': self.available_count,
            'created_at': self.created_at.isoformat()
        }


class BorrowRecord(db.Model):
    __tablename__ = 'borrow_records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='borrowed')  # borrowed, returned

    user = db.relationship('User', backref='borrow_records')
    book = db.relationship('Book', backref='borrow_records')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username,
            'book_id': self.book_id,
            'book_title': self.book.title,
            'borrow_date': self.borrow_date.isoformat(),
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'status': self.status
        }
