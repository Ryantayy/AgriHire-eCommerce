from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, SelectField, EmailField
from wtforms.validators import InputRequired, DataRequired, Length, ValidationError
from agrihire.utilities import user_exists_with_email
import re

def validate_user_already_exists(form, field):
    if user_exists_with_email(field.data):
        raise ValidationError(
            "This email address is already registered.")

def validate_email_format(form, field):
    if not re.match(r'[^@]+@[^@]+\.[^@]+', field.data):
        raise ValidationError("You did not enter a valid email!")
    
def letters_only(form, field):
    if not field.data.isalpha():  # Checks if all characters in the string are alphabetic
        raise ValidationError('This field should contain only letters.')

def validate_phone(self, field):
        if not re.match(r'^\+?[0-9]\d{5,25}$', field.data):
            raise ValidationError("Invalid phone number!")
    
class Strip(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        field.data = field.data.strip() if field.data else field.data

# Basic user form with common fields that are for all type of users: title, firstname, lastname, phone, position + submit button
class BasicUserForm(FlaskForm):
    title = SelectField("Title *", validators=[DataRequired()])
    firstname = StringField("First name *", validators=[InputRequired("Input is required!"),
                                                        DataRequired(
                                                            "Data is required!"),
                                                        Length(
                                                            min=2, max=20, message="Firstname must be between 2 and 20 characters long!"),
                                                        letters_only,
                                                        Strip()])

    lastname = StringField("Last name *", validators=[InputRequired("Input is required!"),
                                                      DataRequired(
                                                          "Data is required!"),
                                                      Length(
                                                          min=2, max=20, message="Lastname must be between 2 and 20 characters long!"),
                                                    letters_only,
                                                      Strip()])

    phone = StringField("Phone *", validators=[InputRequired("Input is required!"),
                                               DataRequired(
                                                   "Data is required!"),
                                               Length(
                                                   min=5, max=25, message="Phone number must be between 5 and 25 characters long!"),
                                               validate_phone,
                                               Strip()])

    submit = SubmitField("Submit")
