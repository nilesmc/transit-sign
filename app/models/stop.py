from app import db
from datetime import datetime
from app.lib import ArrivalService
from app.lib import GeoCodingService
from app.lib import StopService
from sqlalchemy import event, and_, not_
from sqlalchemy.orm import relationship

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