from datetime import datetime
from ..extensions import db


class Building(db.Model):
    __tablename__ = 'buildings'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    address = db.Column(db.String(128))
    floors = db.Column(db.Integer)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.now)

    manager = db.relationship('User', backref='managed_buildings', foreign_keys=[manager_id])
    rooms = db.relationship('Room', backref='building', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'floors': self.floors,
            'manager_id': self.manager_id,
            'manager_name': self.manager.real_name if self.manager else None,
            'room_count': len(self.rooms),
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
