from app import db, login
from sqlalchemy.orm import relationship

class AddressStops(db.Model):
    __tablename__ = 'address_stops'
    address_id = db.Column('address_id', db.Integer, db.ForeignKey('address.id'), primary_key=True)
    stop_id = db.Column('stop_id', db.Integer, db.ForeignKey('stop.id'), primary_key=True)
    address = db.relationship('Address', backref=db.backref('address_stop'))
    stop =  db.relationship('Stop', backref=db.backref('address_stop'))
    active = db.Column(db.Boolean, default=True)

    def __init__(self, stop=None, address=None):
        self.stop = stop
        self.address = address