from app import app, db, login
from datetime import datetime
from flask_login import UserMixin
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
import jwt
from time import time
from .lib import ArrivalService
from .lib import GeoCodingService
from .lib import StopService
from sqlalchemy import event, and_, not_
from sqlalchemy.orm import relationship

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    addresses = db.relationship('Address',
        backref='user',
        lazy='dynamic',
        order_by="desc(Address.active)"
    )
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

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


class Stop(db.Model):
    __tablename__ = 'stop'
    id = db.Column(db.Integer, primary_key=True)
    stop_id = db.Column(db.Integer, index=True, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    latitude = db.Column(db.Float(Precision=64), index=True)
    longitude = db.Column(db.Float(Precision=64), index=True)
    address = db.Column(db.String(512))
    direction = db.Column(db.String(128))
    active = db.Column(db.Boolean, default=True)

    addresses = db.relationship('Address',
                secondary='address_stops',
                back_populates="stops")

    def __repr__(self):
        return '<Stop {}>'.format(self.stop_id)

    def map_name_param(self):
        str = f"map_{self.stop_id}"
        return str

    def get_arrivals(self):
        arrivals = ArrivalService.ArrivalService([self.stop_id]).get_arrivals()

        return arrivals

    # Should Arrivals be its own model?
    def arrivals(self):
        raw_arrivals = self.get_arrivals()
        arrivals = []

        # Should I groom this data in the arrival service.
        for arrival in raw_arrivals:
          eta = arrival.get('@estimated') or arrival.get('@scheduled')
          arrivals.append({
            'description': arrival['@fullSign'],
            'eta': datetime.fromtimestamp(float(eta)/1000),
            'now': datetime.now(),
            'stop_id': arrival['@locid']
           })

        return arrivals


class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, default=True)
    street_address = db.Column(db.String(512))
    city = db.Column(db.String(256), index=True)
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(16))
    latitude = db.Column(db.Float(Precision=64), index=True)
    longitude = db.Column(db.Float(Precision=64), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    stops = db.relationship('Stop',
                secondary='address_stops',
                back_populates="addresses")


    def __repr__(self):
        return '<Address {}>'.format(self.street_address)

    def map_location_param(self):
        str = f"{self.street_address}, {self.city}, {self.state}"
        str = str.replace(" ", "+")
        return str

    def map_name_param(self):
        str = f"map_{self.id}"
        return str

    def get_coordinates(self):
        coordinates = GeoCodingService.GeoCodingService(self.map_location_param()).get_coordinates()
        self.latitude = coordinates['latitude']
        self.longitude = coordinates['longitude']

    def get_stops(self):
        stops = StopService.StopService(self.coordinates()).get_stops()
        if stops is None : return
        new_stops = []
        # # move this onto the stop model
        # stops = []
        # for stop in raw_stops:
        #   stops.append({
        #     'id': stop['@locid'],
        #     'address': stop['@desc'],
        #     'latitude': stop['@lat'],
        #     'longitude': stop['@lng'],
        #     'direction': stop['@dir']
        #    })

        for stop in stops:
            stop_check = db.session.query(Stop).filter(Stop.stop_id == stop['id']).first()
            if not stop_check:
                new_stop = Stop(
                    stop_id=stop['id'],
                    address=stop['address'],
                    latitude=stop['latitude'],
                    longitude=stop['longitude'],
                    direction=stop['direction']
                )
                new_stops.append(new_stop)


        db.session.add_all(new_stops)
        db.session.commit()
        self.add_stops(stops)

    def add_stops(self, stops):
        stop_ids = [stop['id'] for stop in stops if 'id' in stop]
        new_stops = db.session.query(Stop).filter(Stop.stop_id.in_(stop_ids)).all()
        self.stops.extend(new_stops)
        db.session.commit()

    def coordinates(self):
        coordinates =  [
                self.longitude,
                self.latitude
            ]
        return coordinates

    @staticmethod
    def reset_users_active_addresses(mapper, connection, target):
        db.session.query(Address).filter(and_(Address.user_id == target.user_id, Address.id != target.id)).update({"active": False })

event.listen(Address, 'before_insert', Address.reset_users_active_addresses, retval=False)
event.listen(Address, 'before_update', Address.reset_users_active_addresses, retval=False)
