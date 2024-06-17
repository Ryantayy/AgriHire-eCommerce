from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, SelectField, DateField, TimeField, DateTimeField, DateTimeLocalField, IntegerField, HiddenField, DecimalField, RadioField, TextAreaField, validators, MultipleFileField, FileField, TelField
from wtforms.validators import DataRequired, NumberRange, ValidationError, Length, InputRequired, Regexp
from agrihire.utilities import is_equipment_available, is_store_available_for_equipment, get_hire_periods, get_available_equipment, is_equipment_in_cart
from agrihire.customer.forms import PaymentMethodForm
from datetime import datetime, date, timedelta
from flask_wtf.file import FileAllowed

def check_availability(form, field):
    user_id = form.user_id
    sub_category_id = form.sub_category_id.data  # Assuming you store sub_category_id in the form
    start_datetime = form.start_datetime.data
    end_datetime = form.end_datetime.data
    store_id = form.store.data

    equipment_details = get_available_equipment(sub_category_id, start_datetime, end_datetime, user_id, store_id)

    if not equipment_details:
        raise ValidationError('Equipment is not available for the selected time range.')
    
    else:
        # Store the available equipment_id in the form for use when booking
        form.equipment_id.data = equipment_details['equipment_id']
    
    # Check if this equipment is already in the user's cart
    if is_equipment_in_cart(user_id, form.equipment_id.data, start_datetime, end_datetime):
        raise ValidationError('This equipment is already in your cart for the selected dates.')

def validate_name_on_card(form, field):
    if not field.data.replace(' ', '').isalpha():
        raise ValidationError('Name must contain only letters.')
    
def validate_month(form, field):
    try:
        month = int(field.data)
    except ValueError:
        raise ValidationError("Invalid month format. Please enter a valid month between 01 and 12.")

    if month < 1 or month > 12:
        raise ValidationError("Month must be between 01 and 12.")

    current_year = datetime.now().year
    current_month = datetime.now().month
    input_year = int(form.expiration_year.data)

    input_year_full = 2000 + input_year

    if input_year_full == current_year and month < current_month:
        raise ValidationError("Month cannot be in the past.")
    
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
    input_datetime = field.data
    if not isinstance(input_datetime, datetime):
        raise ValidationError("Invalid datetime format. Please enter a valid datetime.")

    current_datetime = datetime.now()

    if input_datetime < current_datetime:
        raise ValidationError("The datetime cannot be in the past. Please select a future date and time.")

    ten_years_later = current_datetime + timedelta(days=365*10)
    if input_datetime > ten_years_later:
        raise ValidationError("The datetime must be within the next 10 years.")
    
def validate_date_order(form, field):
    start_datetime = form.start_datetime.data
    end_datetime = form.end_datetime.data

    # Ensure both fields have valid data before comparing
    if start_datetime and end_datetime:
        if start_datetime >= end_datetime:
            raise ValidationError('The start date/time must be before the end date/time.')

def validate_store_availability(form, field):
    """
    Custom validator to ensure that the selected store can accommodate the equipment booking.
    """
    store_id = field.data
    equipment_id = form.equipment_id.data

    if not is_store_available_for_equipment(store_id, equipment_id):
        raise ValidationError('The equipment is not available at the selected store . Please choose another store.')

def validate_hire_period(form, field):
    sub_category_id = form.sub_category_id.data
    start_datetime = form.start_datetime.data
    end_datetime = form.end_datetime.data

    min_hire_period, max_hire_period = get_hire_periods(sub_category_id)
    
    hire_duration = (end_datetime - start_datetime).days 

    if hire_duration < min_hire_period:
        raise ValidationError(f'Hire period cannot be less than {min_hire_period} days.')

    if hire_duration > max_hire_period:
        raise ValidationError(f'Hire period cannot be more than {max_hire_period} days.')


class StoresForm(FlaskForm):
    search = StringField('Search by store')
    eGrocery = BooleanField('E-Grocery')
    DealShare = BooleanField('DealShare')
    Dmart = BooleanField('DMart')
    Blinkit = BooleanField('Blinkit')
    BigBasket = BooleanField('BigBasket')
    StoreFront = BooleanField('StoreFront')
    Spencers = BooleanField('Spencers')
    onlineGrocery = BooleanField('Online Grocery')

class hireEquipmentForm(FlaskForm):
    def __init__(self, user_id=None, *args, **kwargs):
        super(hireEquipmentForm, self).__init__(*args, **kwargs)
        self.user_id = user_id  # Store user_id as an instance variable

    equipment_id = HiddenField('Equipment ID')
    sub_category_id = HiddenField('Sub Category ID')
    store = SelectField('Store', choices=[], validators=[DataRequired('Please select a store.')], render_kw={"class": "form-control"})
    start_datetime = DateTimeLocalField('Start DateTime', format='%Y-%m-%dT%H:%M', validators=[DataRequired('Please enter a hire period.'), validate_date_range])
    end_datetime = DateTimeLocalField('End DateTime', format='%Y-%m-%dT%H:%M', validators=[DataRequired('Please enter a hire period.'), 
                                                                                           validate_date_range, validate_date_order, validate_hire_period])
    submit = SubmitField('Add To Cart', render_kw={"class": "btn btn-primary"})

class CheckoutForm(FlaskForm):
   # Radio buttons for address selection
    address_type = RadioField('Address Type', choices=[
        ('home', 'Home Address'),
        ('shipping', 'Shipping Address'),
        ('pickup', 'Self-Pickup')
    ], default='home', validators=[validators.DataRequired()])

    # Home address might not need to be filled out again if it's already saved and chosen
    # But if 'shipping' is chosen, this field is needed
    shipping_address = TextAreaField('Shipping Address', validators=[
        validators.Optional(), validators.Length(min=5, message="Address is too short")
    ], render_kw={"placeholder": "Enter new shipping address", "rows": 4})

    # Special instructions text area
    special_instructions = TextAreaField('Special Instructions', render_kw={"rows": 3})

    card_type = RadioField('Card Type', choices=[
        ('MasterCard', 'MasterCard'),
        ('Visa', 'Visa')
    ], default='MasterCard', validators=[InputRequired("Input is required!"),
        DataRequired("Data is required!")])

    digits = TelField('Card number', validators=[
    InputRequired("Input is required!"),
    DataRequired("Data is required!"),
    Regexp(regex="[0-9\s]{13,19}", message="Invalid card number format."),
    Length(min=13, max=19)
    ], render_kw={"placeholder": "xxxx xxxx xxxx xxxx", "autocomplete": "cc-number", "maxlength": "19", "pattern": "[0-9\s]{13,19}", "inputmode": "numeric", "title": "Card number must be 13 to 19 digits long."})

    expiration_month = StringField('Expiration month (MM)', validators=[
        InputRequired("Input is required!"),
        DataRequired("Data is required!"), validate_month
    ], render_kw={"placeholder": "MM", "autocomplete": "cc-exp-month", "maxlength": "2", "pattern": "[0-9]{2}", "inputmode": "numeric", "title": "Expiration month must be 2 digits."})

    expiration_year = StringField('Expiration year (YY)', validators=[
        InputRequired("Input is required!"),
        DataRequired("Data is required!"),
        validate_year
    ], render_kw={"placeholder": "YY", "autocomplete": "cc-exp-year", "maxlength": "2", "pattern": "[0-9]{2}", "inputmode": "numeric", "title": "Expiration year must be 2 digits."})

    security_code = TelField('Security code', validators=[
        InputRequired("Input is required!"),
        DataRequired("Data is required!"),
        Regexp(regex="[0-9\s]{3}", message="Invalid security code format."),
        Length(min=3, max=3)
    ], render_kw={"placeholder": "xxx", "autocomplete": "cc-csc", "maxlength": "3", "pattern": "[0-9]{3}", "inputmode": "numeric", "title": "Security code must be 3 digits."})

    name_on_card = StringField('Name on card', validators=[
        InputRequired("Input is required!"),
        DataRequired("Data is required!"), Length(
        max=40), validate_name_on_card], render_kw={"placeholder": "Name on card"})

    submit = SubmitField('Place Order')

    
class addProductForm(FlaskForm):
    quantity = IntegerField("Quantity *", validators=[DataRequired("Data is required!"),NumberRange(min=0, message="Quantity cannot be a negative value.")])
    category = SelectField("Category *", validators=[DataRequired("Category is required!")], id='category')
    sub_category = SelectField("Subcategory *", validators=[DataRequired("Sub Category is required!")], id='sub_category')
    store = SelectField("Store *", validators=[DataRequired("Store is required!")])
    purchase_date = DateField("Purchase Date *", format='%Y-%m-%d',validators=[DataRequired("Purchase Date is required!")])
    purchase_cost = DecimalField('Purchase Cost *', validators=[DataRequired("Purchase Cost is required!"),NumberRange(min=0, message="Purchase Cost cannot be a negative value.")])
  
    equipment_condition = SelectField("Equipment Condition *", validators=[DataRequired()], choices=[
        ('new', 'New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('out_of_service', 'Out of Service')
    ])
    equipment_status = SelectField("Equipment Status *", validators=[DataRequired()], choices=[
        ('available', 'Available'),
        ('hired', 'Hired'),
        ('unavailable', 'Unavailable'),
        ('removed', 'Removed')
    ])
    submit = SubmitField('Create Product', render_kw={"class": "btn btn-primary"})

 
