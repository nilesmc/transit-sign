from app import db
from datetime import datetime
from app.lib import ArrivalService
from app.lib import GeoCodingService
from app.lib import StopService
from app.models.stop import Stop
from sqlalchemy import event, and_, not_
from sqlalchemy.orm import relationship

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