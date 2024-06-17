from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, SelectField
from wtforms import SelectField, TextAreaField, IntegerField, DecimalField, TimeField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange, InputRequired
from datetime import date
from wtforms import ValidationError

class Strip(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        field.data = field.data.strip() if field.data else field.data

class BasicWorkshopForm(FlaskForm):
    description = TextAreaField(
        'Description *', validators=[DataRequired("Description is required!")])
    length = IntegerField('Length (mins) *', validators=[
                          InputRequired("Input is required!"),
                          NumberRange(min=60, message="Length must be at least 60 minutes.")])
    cost = DecimalField('Cost *', validators=[DataRequired("Cost is required!"),
                                              NumberRange(min=0, message="Cost cannot be a negative value.")])
    
    def validate_start_date(self, field):
        if field.data < date.today():
            raise ValidationError("The start date must be in the future.")

    start_time = TimeField('Start time (E.g. 03:00 pm) *', validators=[DataRequired("Start time is required!")],
                           render_kw={"placeholder": "HH:MM"})
    start_date = DateField('Start date *', validators=[DataRequired("Start date is required!")],
                           render_kw={"placeholder": "DD/MM/YYYY"})
    location = SelectField(
        'Location *', validators=[DataRequired("Location is required!")])

    submit = SubmitField("Submit")