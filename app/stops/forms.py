from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired
from app.models import Stop

class StopForm(FlaskForm):
    stop_id = IntegerField('TriMet Stop ID', validators=[DataRequired()])
    active = BooleanField("Active Address", validators=[DataRequired()])
    submit = SubmitField('Submit')