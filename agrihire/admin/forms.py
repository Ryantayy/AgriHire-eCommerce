from wtforms import ValidationError
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms.fields import PasswordField, FileField, TextAreaField, DateField, StringField, TelField, SubmitField, SelectField, IntegerField, BooleanField, EmailField, HiddenField, RadioField, DecimalField,MultipleFileField
from wtforms.validators import InputRequired, EqualTo, Optional, ValidationError, DataRequired, Regexp, Length, NumberRange
from agrihire.basicUserForms import BasicUserForm, Strip
from agrihire.utilities import user_exists_with_email
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
    
class editAdminProfileForm(BasicUserForm):
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

class paymentMethodForm(FlaskForm):
    card_type = RadioField('Card Type', choices=[
        ('mastercard', 'MasterCard'),
        ('visa', 'Visa')
    ], validators=[DataRequired()])

    digits = TelField('Card number', validators=[
        InputRequired("Input is required!"),
        DataRequired("Data is required!"),
        Regexp(regex="[0-9\s]{13,19}", message="Invalid card number format."),
        Length(min=13, max=19)
    ], render_kw={"placeholder": "xxxx xxxx xxxx xxxx", "autocomplete": "cc-number", "maxlength": "19"})

    expiration_month = StringField('Expiration month (MM)', validators=[
        InputRequired("Input is required!"),
        DataRequired("Data is required!"), validate_month
    ], render_kw={"placeholder": "MM", "autocomplete": "cc-exp-month", "maxlength": "2"})

    expiration_year = StringField('Expiration year (YY)', validators=[
        InputRequired("Input is required!"),
        DataRequired("Data is required!"),
        validate_year
    ], render_kw={"placeholder": "YY", "autocomplete": "cc-exp-year", "maxlength": "2"})

    security_code = TelField('Security code', validators=[
        InputRequired("Input is required!"),
        DataRequired("Data is required!"),
        Regexp(regex="[0-9\s]{3}", message="Invalid security code format."),
        Length(min=3, max=3)
    ], render_kw={"placeholder": "xxx", "autocomplete": "cc-csc", "maxlength": "3"})

    name_on_card = StringField('Name on card', validators=[
        InputRequired("Input is required!"),
        DataRequired("Data is required!"), Length(
        max=40), validate_name_on_card], render_kw={"placeholder": "Name on card"})


class mainCategory(FlaskForm):
    category_name = StringField('Category Name *', validators=[ InputRequired("Name is required!")])
    
    submit = SubmitField('Add Category', render_kw={"class": "btn btn-primary"})

class subCategory(FlaskForm):
    category = SelectField("Category *", validators=[DataRequired("Category is required!")], id='category')
    name = StringField('Sub Category Name *', validators=[ InputRequired("Name is required!")])
    hire_cost = DecimalField('Hire Cost / Hour *', validators=[DataRequired("Hire Cost is required!"),NumberRange(min=0, message="Hire Cost cannot be a negative value.")])
    product_images = MultipleFileField("Product Images (Max 3 images)", validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only (jpg, png, jpeg)!')
    ])    
    description = TextAreaField('Description *', validators=[DataRequired()])
    weight = IntegerField('Weight *', validators=[InputRequired("Input is required!"),NumberRange(min=0, message="Weight cannot be a negative value.")])
    dimension  = StringField("Dimension  *", validators=[DataRequired()])
    shipping_price = DecimalField('Shipping Price *', validators=[DataRequired("Shipping Price is required!"),NumberRange(min=0, message="Shipping Price cannot be a negative value.")])
    
    submit = SubmitField('Add SubCategory', render_kw={"class": "btn btn-primary"})
    
    def validate_product_images(self, field):
        if len(field.data) > 3:
            raise ValidationError('You can only upload a maximum of 3 images.')
        
class EditSubCategoryForm(FlaskForm):
    hire_cost = DecimalField('Hire Cost *', validators=[DataRequired("Hire Cost is required!"),NumberRange(min=0, message="Hire Cost cannot be a negative value.")])   
    description = TextAreaField('Description')
    category = TextAreaField('Category')
    subcategory = TextAreaField('Subcategory')
    weight = IntegerField('Weight')
    dimension  = StringField("Dimension")
    shipping_price = DecimalField('Shipping Price *', validators=[DataRequired("Shipping Price is required!"),NumberRange(min=0, message="Shipping Price cannot be a negative value.")])
    min_hire_period = IntegerField('Minhire Period *', validators=[DataRequired("Minhire Period is required!"),NumberRange(min= 1, max =30, message="Minhire Period must be in the rang of 1 and 30.")])
    max_hire_period = IntegerField('Maxhire Period *', validators = [DataRequired("Maxhire Period is required!"), NumberRange(min= 1, max =30, message="Maxhire Period must be in the rang of 1 and 30.")])
    
    def validate_min_hire_period(self, field):
        if self.min_hire_period.data is not None and field.data > self.max_hire_period.data:
            raise ValidationError("Min Hire Period cannot be greater than Max Hire Period.")

class StoreForm(FlaskForm):
    store_name = StringField('Store Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    image = FileField('Store Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'svg'], 'Images only!')])
    submit = SubmitField('Add Store')
    
class addNationalManagerForm(BasicUserForm):
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
    address = TextAreaField("Address *", validators=[InputRequired("Input is required!"),
                                                                   DataRequired("Description is required!"), Strip()])
    

class editNationalManagerForm(BasicUserForm):
    original_email = HiddenField()
    email = EmailField("Email *", validators=[InputRequired("Input is required!"),
                                              DataRequired(
                                                  "Data is required!"),
                                              Length(
                                                  min=5, max=50, message="Email must be between 5 and 50 characters long!"),
                                              validate_email_format, validate_user_already_exists_excluding_self])
    

    address = TextAreaField("Address *", validators=[InputRequired("Input is required!"),
                                                                   DataRequired("Description is required!"), Strip()])
    
    password = PasswordField("Password * (at least 8 characters with one uppercase letter, one lowercase letter, and one number)",
                             validators=[InputRequired("Input is required!"),
                                         DataRequired("Data is required!"),
                                         Length(
                                             min=8, max=40, message="Password must be between 8 and 40 characters long"),
                                         EqualTo("password_confirm", message="Passwords must match!"), validate_password_complexity])
    
    password_confirm = PasswordField("Confirm password *", validators=[InputRequired("Input is required!"),
                                                                       DataRequired("Data is required!")])