from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, EmailField, FileField, TextAreaField, DateField, StringField, SelectField, SubmitField,IntegerField, BooleanField
from wtforms.validators import InputRequired, DataRequired, Length, EqualTo, Email, ValidationError,Optional, NumberRange
from agrihire.basicUserForms import BasicUserForm, Strip
from agrihire.utilities import user_exists_with_email
from datetime import date
import re

def validate_user_already_exists(form, field):
    if user_exists_with_email(field.data):
        raise ValidationError(
            "This email address is already registered.")


def validate_email_format(form, field):
    if not re.match(r'[^@]+@[^@]+\.[^@]+', field.data):
        raise ValidationError("You did not enter a valid email!")


def validate_password_complexity(form, field):
    if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', field.data):
        raise ValidationError(
            "Password should be at least 8 characters, including one uppercase letter, one lowercase letter, and one number!")
    
def validate_user_not_exists(form, field):
    if user_exists_with_email(field.data) == False:
        raise ValidationError(
            "There is no registered account with that email.")

def validate_date_of_birth(form, field):
    if field.data < date(1900, 1, 1):
        raise ValidationError(
            "Date of birth cannot be before January 1, 1900.")
    # Checks that the date of birth is at least 15 years ago
    if field.data > date.today().replace(year=date.today().year - 16):
        raise ValidationError("Member must be at least 16 years old.")
        

class LoginForm(FlaskForm):
    email = EmailField("Email *", validators=[InputRequired("Input is required!"),
                                              DataRequired(
                                                  "Data is required!"),
                                              Length(
        min=5, max=50, message="Email must be between 5 and 50 characters long!"),
        validate_email_format, validate_user_not_exists])

    password = PasswordField("Password *", validators=[InputRequired("Input is required!"),
                                                       DataRequired(
                                                           "Data is required!"),
                                                       Length(min=8, max=40, message="Password must be between 8 and 40 characters long!")])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField("Login")
    
class RegisterForm(BasicUserForm):
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

    date_of_birth = DateField("Date of birth *", format='%Y-%m-%d',
                              validators=[DataRequired(), validate_date_of_birth])

    address = TextAreaField("Address *", validators=[InputRequired("Input is required!"),
                                                                   DataRequired("Description is required!"), Strip()])

class PasswordResetForm(FlaskForm):
    email = EmailField("Email *", validators=[InputRequired("Input is required!"),
                                              DataRequired(
                                                  "Data is required!"),
                                              Length(
                                                  min=5, max=50, message="Email must be between 5 and 50 characters long!"),
                                              validate_email_format])
    
    password = PasswordField("Password * (at least 8 characters with one uppercase letter, one lowercase letter, and one number)",
                             validators=[InputRequired("Input is required!"),
                                         DataRequired("Data is required!"),
                                         Length(
                                             min=8, max=40, message="Password must be between 8 and 40 characters long"),
                                         EqualTo("password_confirm", message="Passwords must match!"), validate_password_complexity])

    password_confirm = PasswordField("Confirm password *", validators=[InputRequired("Input is required!"),
                                                                       DataRequired("Data is required!")])


