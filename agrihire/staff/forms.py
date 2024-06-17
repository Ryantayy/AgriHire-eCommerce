from wtforms import ValidationError
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms.fields import PasswordField, DecimalField, TextAreaField, DateField, StringField,SubmitField, SelectField, IntegerField, EmailField, HiddenField
from wtforms.validators import InputRequired, ValidationError, DataRequired, Length, NumberRange
from agrihire.basicUserForms import BasicUserForm, Strip
from agrihire.utilities import get_return_time_for_equipment, is_service_date_within_booking_period, user_exists_with_email
from datetime import datetime, date
import re

def validate_name_on_card(form, field):
    if not field.data.replace(' ', '').isalpha():
        raise ValidationError('Name must contain only letters.')

def validate_password_complexity(form, field):
    if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', field.data):
        raise ValidationError(
            "Password should contain at least 8 characters, one uppercase letter, one lowercase letter, and one number!")

def validate_month(form, field):
    month = int(field.data)
    if month < 1 or month > 12:
        raise ValidationError("Month must be between 01 and 12.")

def validate_user_already_exists(form, field):
    if user_exists_with_email(field.data):
        raise ValidationError(
            "This email address is already registered.")
    
def validate_user_already_exists_excluding_self(form, field):
    if field.data != form.original_email.data:
        if user_exists_with_email(field.data):
            raise ValidationError("This email address is already registered by another user.")

def validate_email_format(form, field):
    if not re.match(r'[^@]+@[^@]+\.[^@]+', field.data):
        raise ValidationError("You did not enter a valid email!")
    
def validate_year(form, field):
    try:
        # Assuming the input is in "YY" format and all years are 2000s.
        input_year = 2000 + int(field.data)
    except ValueError:
        # This catch block ensures any non-integer input is flagged as an invalid format.
        raise ValidationError("Invalid year format.")

    current_year = datetime.now().year

    # Check if the input year is more than 10 years in the future.
    if input_year - current_year > 10:
        raise ValidationError("Year must be within the next 10 years.")

    # Check if the input year is in the past.
    if input_year < current_year:
        raise ValidationError("Year cannot be in the past.")


def validate_service_date(form, field):
    if field.data < datetime.today().date():
        raise ValidationError('Service date cannot be in the past.')

    service_date = field.data
    equipment_id = form.equipment_id.data

    if is_service_date_within_booking_period(equipment_id, service_date):
        raise ValidationError('The service date is within the borrowing period for this equipment. Please choose another date.')

def validate_retire_date(form, field):
    if field.data < datetime.today().date():
        raise ValidationError('retire date cannot be in the past.')

    retire_date = field.data
    equipment_id = form.equipment_id.data
    latest_checkout_next_day = get_return_time_for_equipment(equipment_id)

    if latest_checkout_next_day and latest_checkout_next_day >= retire_date:
        raise ValidationError(
            'The retire date is within the borrowing period for this equipment. Please book after {}'.format(latest_checkout_next_day)
        )

class EditStaffProfileForm(BasicUserForm):
    original_email = HiddenField()
    email = EmailField("Email *", validators=[InputRequired("Input is required!"),
                                              DataRequired(
                                                  "Data is required!"),
                                              Length(
                                                  min=5, max=50, message="Email must be between 5 and 50 characters long!"),
                                              validate_email_format, validate_user_already_exists_excluding_self])
    address = StringField("Address *", validators=[InputRequired("Input is required!"),
                                                   DataRequired(
                                                       "Data is required!"),
                                                   Length(min=2, max=255, message="Address must be between 2 and 255 characters long!")])


class changePasswordForm(FlaskForm):
    current_password = PasswordField("Current password *", validators=[DataRequired()])
    new_password = PasswordField("New Password *",
                             validators=[InputRequired("Input is required!"),
                                         DataRequired("Data is required!"),
                                         Length(
                                             min=8, max=40, message="Password must be between 8 and 40 characters long"), validate_password_complexity])
    submit = SubmitField("Change password")


class EditEquipmentForm(FlaskForm):
    sub_category_name = StringField('Sub Category Name')
    serial_number = StringField('Serial Number')
    equipment_condition = SelectField(
        'Equipment Condition', 
        choices=[
            ('new', 'New'), 
            ('good', 'Good'), 
            ('fair', 'Fair'), 
            ('poor', 'Poor')
        ], 
        validators=[DataRequired()]
    )

class editEnquiryForm(FlaskForm):
    customer = StringField('Customer ID')
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    email = StringField('Email')
    subject = StringField('Subject')
    message_text = TextAreaField("Customer'message")
    reply_text = TextAreaField("Message Reply *",validators=[DataRequired()])

class createNotificationForm(FlaskForm):
    recipient = SelectField('Recipient')
    message = TextAreaField("Message", validators=[InputRequired("Input is required!"),
                                                                DataRequired("Please enter message!")])
    submit = SubmitField("Create")

class RequestServiceForEquipmentForm(FlaskForm):
    equipment_id = IntegerField('Equipment ID')
    service_date = DateField('Service Date *', format='%Y-%m-%d', validators=[DataRequired(), validate_service_date])
    description = TextAreaField('Description *', validators=[DataRequired()])
    cost = DecimalField('Cost *', places=2, validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Submit')


class EquipmentRetireForm(FlaskForm):
    equipment_id = IntegerField('Equipment ID')
    retire_date = DateField('Retire Date *', format='%Y-%m-%d', validators=[DataRequired(), validate_retire_date])
    submit = SubmitField('Submit')