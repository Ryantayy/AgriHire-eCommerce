from wtforms import ValidationError
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms.fields import PasswordField, FileField, TextAreaField, DateField, StringField, TelField, SubmitField, SelectField, IntegerField, BooleanField, EmailField, HiddenField, RadioField,DecimalField
from wtforms.validators import InputRequired, EqualTo, Optional, ValidationError, DataRequired, Regexp, Length, NumberRange
from agrihire.basicUserForms import BasicUserForm, Strip
from agrihire.utilities import user_exists_with_email, check_existing_promotions,get_return_time_for_equipment
from datetime import datetime, date, timedelta
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

def validate_date_range(form, field):
    input_date = field.data
    if not isinstance(input_date, date):
        raise ValidationError("Invalid date format. Please enter a valid date.")

    current_date = datetime.now().date()

    if input_date < current_date:
        raise ValidationError("The datetime cannot be in the past. Please select a future date and time.")

    ten_years_later = current_date + timedelta(days=365*10)
    if input_date > ten_years_later:
        raise ValidationError("The datetime must be within the next 10 years.")
    
def validate_date_order(form, field):
    start_date = form.start_date.data
    end_date = form.end_date.data

    # Ensure both fields have valid data before comparing
    if start_date and end_date:
        if start_date >= end_date:
            raise ValidationError('The start date/time must be before the end date/time.')
        
def validate_discount_rate(form, field):
    if field.data < 0 or field.data > 100:
        raise ValidationError('Discount rate must be between 0 and 100 percent.')
    
def validate_no_existing_promotion(form, field):
    equipment_id = form.equipment.data
    start_date = form.start_date.data
    end_date = form.end_date.data
    current_promotion_id = form.promotion_id.data

    if start_date and end_date:
        overlapping = check_existing_promotions(equipment_id, start_date, end_date, current_promotion_id)
        if overlapping:
            raise ValidationError('A promotion already exists for the selected equipment within the specified date range.')

def validate_service_date(form, field):
    if field.data < datetime.today().date():
        raise ValidationError('Service date cannot be in the past.')

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
                  
class EditManagerProfileForm(BasicUserForm):
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

class addStaffForm(BasicUserForm):
    email = EmailField("Email *", validators=[InputRequired("Input is required!"),
                                              DataRequired(
                                                  "Data is required!"),
                                              Length(
                                                  min=5, max=50, message="Email must be between 5 and 50 characters long!"),
                                              validate_email_format, validate_user_already_exists])
    
    password = PasswordField("Password * (at least 8 characters with one uppercase letter, one lowercase letter, and one number)",
                             validators=[InputRequired("Input is required!"),
                                         DataRequired("Data is required!"),
                                         Length(
                                             min=8, max=40, message="Password must be between 8 and 40 characters long"),
                                         EqualTo("password_confirm", message="Passwords must match!"), validate_password_complexity])

    password_confirm = PasswordField("Confirm password *", validators=[InputRequired("Input is required!"),
                                                                       DataRequired("Data is required!")])
    profile_image = FileField("Profile image * (Max 1 image)", validators=[
                              FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])

    address = TextAreaField("Address *", validators=[InputRequired("Input is required!"),
                                                                   DataRequired("Description is required!"), Strip()])
    store = SelectField("Store *", validators=[DataRequired()])

class editStaffForm(BasicUserForm):
    original_email = HiddenField()
    email = EmailField("Email *", validators=[InputRequired("Input is required!"),
                                              DataRequired(
                                                  "Data is required!"),
                                              Length(
                                                  min=5, max=50, message="Email must be between 5 and 50 characters long!"),
                                              validate_email_format, validate_user_already_exists_excluding_self])
    
    profile_image = FileField("Profile image * (Max 1 image)", validators=[
                              FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])

    address = TextAreaField("Address *", validators=[InputRequired("Input is required!"),
                                                                   DataRequired("Description is required!"), Strip()])
    store = SelectField("Store *", validators=[DataRequired()])

class addPromotionForm(FlaskForm):
    title = StringField("Title *", validators=[InputRequired("Input is required!"),
                                              DataRequired(
                                                  "Data is required!"),
                                              Length(
                                                  min=5, max=50, message="Title must be between 5 and 50 characters long!")])
    
    equipment = SelectField("Equipment *", validators=[DataRequired()])

    image = FileField("Image * (Max 1 image)", validators=[
                            FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    
    description = TextAreaField("Description *", validators=[InputRequired("Input is required!"),
                                                                   DataRequired("Description is required!"), Strip()])

    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired('Please enter a start date.'), validate_date_range])

    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired('Please enter an end date.'), 
                                                                                           validate_date_range, validate_date_order, validate_no_existing_promotion])
    
    discount_rate = IntegerField("Discount Rate *", validators=[InputRequired("Input is required!"),
                                                                DataRequired("Discount Rate is required!"), validate_discount_rate])
    
    promotion_id = HiddenField()
    
class editPromotionForm(addPromotionForm):
    promotion_id = HiddenField()
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired('Please enter a start date.')])

    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired('Please enter an end date.'), validate_date_order, validate_no_existing_promotion])
    submit = SubmitField('Save Changes')

class createNotificationForm(FlaskForm):
    recipient = SelectField('Recipient')
    message = TextAreaField("Message", validators=[InputRequired("Input is required!"),
                                                                DataRequired("Please enter message!")])
    submit = SubmitField("Create")
    
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
    
class RequestServiceForEquipmentForm(FlaskForm):
    equipment_id = IntegerField('Equipment ID')
    service_date = DateField('Service Date *', format='%Y-%m-%d', validators=[DataRequired(), validate_service_date])
    description = TextAreaField('Description *', validators=[DataRequired()])
    cost = DecimalField('Cost *', places=2, validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Submit')

class StoreForm(FlaskForm):
    store_name = StringField('Store Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    image = FileField('Store Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'svg'], 'Images only!')])
    submit = SubmitField('Add Store')

class MgrEquipmentRetireForm(FlaskForm):
    equipment_id = IntegerField('Equipment ID')
    retire_date = DateField('Retire Date *', format='%Y-%m-%d', validators=[DataRequired(), validate_retire_date])
    submit = SubmitField('Submit')