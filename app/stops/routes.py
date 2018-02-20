from app import db
from app.stops import bp
from flask import render_template, flash, redirect, request, url_for
from app.stops.forms import StopForm
from flask_login import current_user, login_required
from app.models import Address, Stop
from datetime import datetime
from flask_googlemaps import GoogleMaps, Map

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/stops', methods=['GET', 'POST'])
@login_required
def index():
    active_address = db.session.query(Address).filter(Address.user_id == current_user.id, Address.active == True).first()
    # consider moving this as callback for Address
    active_address.get_stops()

    return render_template('stops/index.html', title='Stops', address=active_address)

@bp.route('/stops/<stop_id>', methods=['GET', 'POST'])
@login_required
def edit(stop_id):
    stop = db.session.query(Stop).filter(Stop.id == stop_id).first()
    form = StopForm()

    if form.validate_on_submit():
        db.session.query(Stop).filter(Stop.id == stop.id).update({Stop.active: form.active.data, Stop.stop_id: form.id.data
        })
        # Stop.get_arrivals()
        db.session.commit()

        flash('Your stop has been updated!')
        return redirect(url_for('stop_index'))
    elif request.method == 'GET':
        form.active.data = stop.active
        form.stop_id.data = stop.stop_id

    return render_template('stops/edit.html', title='Edit Stop', form=form)
