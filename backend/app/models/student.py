from datetime import datetime
from ..extensions import db


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    student_no = db.Column(db.String(20), unique=True, nullable=False)
    gender = db.Column(db.String(4))
    college = db.Column(db.String(64))
    major = db.Column(db.String(64))
    class_name = db.Column(db.String(32))
    enrollment_year = db.Column(db.Integer)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    check_in_date = db.Column(db.Date)
    check_out_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'student_no': self.student_no,
            'gender': self.gender,
            'college': self.college,
            'major': self.major,
            'class_name': self.class_name,
            'enrollment_year': self.enrollment_year,
            'room_id': self.room_id,
            'check_in_date': self.check_in_date.isoformat() if self.check_in_date else None,
            'check_out_date': self.check_out_date.isoformat() if self.check_out_date else None,
            'user': self.user.to_dict() if self.user else None,
            'room': self.room.to_dict() if self.room else None,
        }
