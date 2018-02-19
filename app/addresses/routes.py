from app import db
from flask import render_template, flash, redirect, request, url_for
from app.forms import AddressForm
from flask_login import current_user, login_required
from app.models import User, Address, Stop
from datetime import datetime
from flask_googlemaps import GoogleMaps, Map

@bp.route('/address', methods=['GET', 'POST'])
@login_required
def address_index():
    form = AddressForm()

    if form.validate_on_submit():
        address = Address(active=form.active.data, street_address=form.street_address.data, city=form.city.data, state=form.state.data, zip_code=form.zip_code.data, latitude=0,longitude=0, user=current_user)
        db.session.add(address)
        address.get_coordinates()
        db.session.commit()
        flash('Your address has been added!')
        return redirect(url_for('address_index'))
    return render_template('addresses/index.html', title='Addresses', form=form)

@bp.route('/address/<address_id>', methods=['GET', 'POST'])
@login_required
def edit_address(address_id):
    address = db.session.query(Address).filter(Address.id == address_id).first()
    form = AddressForm()

    if form.validate_on_submit():
        db.session.query(Address).filter(Address.id == address_id).update({Address.active: form.active.data, Address.street_address: form.street_address.data, Address.city: form.city.data, Address.state: form.state.data, Address.zip_code: form.zip_code.data})

        address.get_coordinates()
        db.session.commit()

        flash('Your address has been updated!')
        return redirect(url_for('address_index'))
    elif request.method == 'GET':
        form.active.data = address.active
        form.street_address.data = address.street_address
        form.city.data = address.city
        form.state.data = address.state
        form.zip_code.data = address.zip_code
    return render_template('addresses/edit.html', title='Edit Address', form=form)