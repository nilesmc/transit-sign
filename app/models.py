from app import app, db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
import jwt
from time import time
from .lib import GeoCodingService
from sqlalchemy import event, and_

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    stops = db.relationship('Stop', backref='user', lazy='dynamic')
    addresses = db.relationship('Address', backref='user', lazy='dynamic')
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
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Stop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stop_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    active = db.Column(db.Boolean, default=True)
    # - Lines
    # - Bus / Train
    # - Lat
    # - Long
    # - Direction

    def __repr__(self):
        return '<Stop {}>'.format(self.stop_id)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, default=True)
    street_address = db.Column(db.String(512))
    city = db.Column(db.String(256), index=True)
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(16))
    latitude = db.Column(db.Float(Precision=64), primary_key=True)
    longitude = db.Column(db.Float(Precision=64), primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

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

    @staticmethod
    def reset_users_active_addresses(mapper, connection, target):
        if target.active:
            db.session.query(Address).filter(and_(Address.user_id == target.user_id, Address.active == True)).update({"active": False })

event.listen(Address, 'before_insert', Address.reset_users_active_addresses, retval=False)

event.listen(Address, 'before_update', Address.reset_users_active_addresses, retval=False)

