from app import db
from flask import request
from flask_login import current_user, login_required
from app.models import User, Address, Stop
from flask import jsonify

@bp.route('/arrivals', methods=['GET', 'POST'])
@login_required
def arrivals():
    # should get a user token instead of relying on current user
    active_address = current_user.addresses.first()

    stop_arrivals = list(map(lambda stop:stop.arrivals(), active_address.stops))

    return jsonify({'arrivals': stop_arrivals })

