from datetime import datetime
from ..extensions import db


class AccessLog(db.Model):
    __tablename__ = 'access_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False)
    direction = db.Column(db.String(4), nullable=False)
    method = db.Column(db.String(16), nullable=False, default='face')
    confidence = db.Column(db.Float)
    is_authorized = db.Column(db.Boolean, nullable=False)
    snapshot_path = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)

    building = db.relationship('Building', backref='access_logs')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.real_name if self.user else '未知',
            'building_id': self.building_id,
            'building_name': self.building.name if self.building else None,
            'direction': self.direction,
            'method': self.method,
            'confidence': self.confidence,
            'is_authorized': self.is_authorized,
            'snapshot_path': self.snapshot_path,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
