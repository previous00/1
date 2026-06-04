from datetime import datetime
from ..extensions import db


class Visitor(db.Model):
    __tablename__ = 'visitors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    id_card = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    reason = db.Column(db.String(256))
    visit_target_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'))
    applicant_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(16), default='pending')
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    visit_start = db.Column(db.DateTime)
    visit_end = db.Column(db.DateTime)
    actual_enter = db.Column(db.DateTime)
    actual_leave = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now)

    visit_target = db.relationship('User', foreign_keys=[visit_target_id], backref='visitors_received')
    building = db.relationship('Building', backref='visitors')
    applicant = db.relationship('User', foreign_keys=[applicant_id], backref='visitor_applications')
    approver = db.relationship('User', foreign_keys=[approved_by])

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'id_card': self.id_card,
            'phone': self.phone,
            'reason': self.reason,
            'visit_target_id': self.visit_target_id,
            'visit_target_name': self.visit_target.real_name if self.visit_target else None,
            'building_id': self.building_id,
            'building_name': self.building.name if self.building else None,
            'applicant_id': self.applicant_id,
            'applicant_name': self.applicant.real_name if self.applicant else None,
            'status': self.status,
            'approved_by': self.approved_by,
            'approver_name': self.approver.real_name if self.approver else None,
            'visit_start': self.visit_start.isoformat() if self.visit_start else None,
            'visit_end': self.visit_end.isoformat() if self.visit_end else None,
            'actual_enter': self.actual_enter.isoformat() if self.actual_enter else None,
            'actual_leave': self.actual_leave.isoformat() if self.actual_leave else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
