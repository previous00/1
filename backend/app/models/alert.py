from datetime import datetime
from ..extensions import db


class Alert(db.Model):
    __tablename__ = 'alerts'

    id = db.Column(db.Integer, primary_key=True)
    access_log_id = db.Column(db.Integer, db.ForeignKey('access_logs.id'))
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'))
    alert_type = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(256))
    snapshot_path = db.Column(db.String(256))
    status = db.Column(db.String(16), default='unread')
    handled_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    handled_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now)

    access_log = db.relationship('AccessLog', backref='alerts')
    building = db.relationship('Building', backref='alerts')
    handler = db.relationship('User', foreign_keys=[handled_by])

    def to_dict(self):
        return {
            'id': self.id,
            'access_log_id': self.access_log_id,
            'building_id': self.building_id,
            'building_name': self.building.name if self.building else None,
            'alert_type': self.alert_type,
            'description': self.description,
            'snapshot_path': self.snapshot_path,
            'status': self.status,
            'handled_by': self.handled_by,
            'handler_name': self.handler.real_name if self.handler else None,
            'handled_at': self.handled_at.isoformat() if self.handled_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
