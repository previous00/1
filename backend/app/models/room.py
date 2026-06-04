from ..extensions import db


class Room(db.Model):
    __tablename__ = 'rooms'
    __table_args__ = (db.UniqueConstraint('building_id', 'room_number'),)

    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False)
    room_number = db.Column(db.String(16), nullable=False)
    floor = db.Column(db.Integer)
    capacity = db.Column(db.Integer, default=4)
    current_count = db.Column(db.Integer, default=0)

    students = db.relationship('Student', backref='room', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'building_id': self.building_id,
            'building_name': self.building.name if self.building else None,
            'room_number': self.room_number,
            'floor': self.floor,
            'capacity': self.capacity,
            'current_count': self.current_count,
        }
