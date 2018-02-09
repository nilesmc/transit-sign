from app import app, db
from flask import render_template, flash, redirect, request, url_for
from app.forms import LoginForm, RegistrationForm, EditProfileForm, AddressForm, \
    ResetPasswordRequestForm, ResetPasswordForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Address
from datetime import datetime
from app.email import send_password_reset_email
from flask_googlemaps import GoogleMaps, Map

# USER ROUTES #
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

# No Login Required
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html', title='Home')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', title='About')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# Login Required
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    stops = [
        {'stop_id': '1234', 'next_arrival_time': '1pm'},
        {'stop_id': '5432', 'next_arrival_time': '1am'}
    ]
    return render_template('user.html', user=user, stops=stops)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
# Password Management
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

# ADDRESS ROUTES #
@app.route('/address', methods=['GET', 'POST'])
@login_required
def address_index():
    form = AddressForm()
    if form.validate_on_submit():
        all_addresses = Address()
        address = Address(active=form.active.data, street_address=form.street_address.data, city=form.city.data, state= form.state.data, zip_code=form.zip_code.data, latitude=0,longitude=0, user=current_user)
        db.session.add(address)
        address.get_coordinates()
        db.session.commit()
        flash('Your address has been added!')
        return redirect(url_for('index'))
    return render_template('addresses_index.html', title='Addresses', form=form)

@app.route('/address/<adddress_id>', methods=['GET', 'POST'])
@login_required
def edit_address():
    form = AddressForm()
    # look up address id from param, make sure it is in list of current user, feed it to the form
    # form = AddressForm(address)
    if form.validate_on_submit():
        address = Address(active=form.active.data, street_address=form.street_address.data, city=form.city.data, state= form.state.data, zip_code=form.zip_code.data, latitude=0,longitude=0, user=current_user)
        db.session.add(address)
        db.session.commit()
        flash('Your address has been added!')
        return redirect(url_for('index'))
    return render_template('edit_addresses.html', title='Addresses', form=form)


# STOP ROUTES #
@app.route('/stops', methods=['GET', 'POST'])
@login_required
def stops_index():
    return render_template('stops_index.html', title='Stops')

