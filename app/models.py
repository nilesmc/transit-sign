from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

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

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Stop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stop_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
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
    state = db.String(2)
    zip_code = db.String(16)
    latitude = db.Column(db.Float(Precision=64), primary_key=True)
    longitude = db.Column(db.Float(Precision=64), primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Address {}>'.format(self.street_address)
