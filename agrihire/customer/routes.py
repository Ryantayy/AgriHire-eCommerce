from flask import Blueprint, render_template, flash, redirect, url_for, session
from flask import request
from agrihire import my_hashing
import re
from agrihire.utilities import add_messsage, get_all_stores_list, get_user_full_name, update_customer_profile, get_customer_by_user_id, get_user_titles, get_user_by_email, hash_password, reset_password, get_customer_bookings, get_customer_payment_methods, customer_add_payment_method, get_shop_cart_items, calculate_subtotals,get_all_category,get_all_stores, get_customer_orders, delete_payment_method, count_num_of_product_with_category, cancel_order, get_sub_category_by_category, format_currency, get_booking_info_by_order_id, get_order_by_order_id, retrieve_notifications, get_customer_by_user_id
from agrihire.customer.forms import EditCustomerProfileForm, PaymentMethodForm, changePasswordForm, enquiryForm
from datetime import datetime, timedelta

customer = Blueprint("customer", __name__, template_folder="templates")

# functions
def check_password(user, user_password):
    # Compare hashed password with the password stored in db
    db_password = user['password']
    if my_hashing.check_value(db_password, user_password, salt='myhashsalt'):
        return True
    else:
        return False

def check_auth():
    if not 'loggedin' in session:
        flash("Please login first.", "danger")
        return redirect(url_for('auth.login'))

    if session['role_id'] != 1:
        flash("Invalid action! Back to home page.", "danger")
        return redirect(url_for('main.home'))
    return None

def flash_form_errors(form):
    if form.errors:
        for error_messages in form.errors.values():
            for error in error_messages:
                flash(f"{error}", "danger")

#getting data for the menu
@customer.context_processor
def inject_menu():
    categories = get_all_category()
    for category in categories:
        sub_categories = get_sub_category_by_category(category['category_id'])
        category['sub_categories'] = sub_categories
    stores = get_all_stores()

    #Retrieve notifications
    user_id = session.get('user_id')
    notifications, today_message_count = retrieve_notifications(user_id)

    return dict(inject_categories=categories, stores=stores, notifications=notifications, today_message_count=today_message_count)

@customer.context_processor
def inject_cart():
    if 'loggedin' in session:
        user_id = session['user_id']
        shop_cart_items = get_shop_cart_items(user_id)
        item_subtotal, gst, subtotal, shipping_total = calculate_subtotals(shop_cart_items)
    else:
        shop_cart_items = []
        item_subtotal = "$0.00"
        gst = "$0.00"
        subtotal = "$0.00"

    return dict(shop_cart_items=shop_cart_items, item_subtotal=item_subtotal, gst=gst, subtotal=subtotal)

@customer.route("/dashboard", methods=["GET"])
def dashboard():
    # Check authentication and authorisation
    auth_response = check_auth()
    if auth_response:
        return auth_response

    return redirect(url_for('customer.account_orders'))

@customer.route("/account_settings", methods=["GET", "POST"])
def account_settings():
    # Check authentication and authorisation
    auth_response = check_auth()
    if auth_response:
        return auth_response

    form = EditCustomerProfileForm()
    password_form = changePasswordForm() 
    user = get_customer_by_user_id(session['user_id'])

    user_titles = get_user_titles()
    form.title.choices = [(title, title) for title in user_titles]

    if form.validate_on_submit():
        title = form.title.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        phone = form.phone.data
        date_of_birth = form.date_of_birth.data
        address = form.address.data

        # Update the user profile
        update_customer_profile(title, firstname, lastname, email, phone, address, date_of_birth)
        session['email'] = email
        flash("Profile updated successfully!", "success")
        return redirect(url_for('customer.dashboard'))
    else:
        form.title.data = user['title']
        form.firstname.data = user['first_name']
        form.lastname.data = user['last_name']
        form.original_email.data = user['email']
        form.email.data = user['email']
        form.phone.data = user['phone']
        form.date_of_birth.data = user['date_of_birth']
        form.address.data = user['address']

    flash_form_errors(form)
    return render_template("account_settings.html", form=form, password_form=password_form)

@customer.route("/change_password", methods=["GET", "POST"])
def change_password():
    # Check authentication and authorisation
    auth_response = check_auth()
    if auth_response:
        return auth_response

    #Retrieve user details
    form = EditCustomerProfileForm()
    user = get_customer_by_user_id(session['user_id'])
    user_titles = get_user_titles()
    form.title.choices = [(title, title) for title in user_titles]

    form.title.data = user['title']
    form.firstname.data = user['first_name']
    form.lastname.data = user['last_name']
    form.original_email.data = user['email']
    form.email.data = user['email']
    form.phone.data = user['phone']
    form.date_of_birth.data = user['date_of_birth']
    form.address.data = user['address']

    password_form = changePasswordForm()
    
    if password_form.validate_on_submit():
        email = session['email']
        current_password = password_form.current_password.data
        new_password = password_form.new_password.data

        # Check if the current password is correct
        email = session['email']
        user = get_user_by_email(email)
        if check_password(user, current_password):
            hashed_password = hash_password(new_password)
            reset_password(email, hashed_password)
            flash("Password changed successfully!", "success")
        else:
            flash("Incorrect password.", "danger")

        return redirect(url_for('customer.dashboard'))

    flash_form_errors(password_form)
    return render_template("account_settings.html", form=form, password_form=password_form)

@customer.route("/account_orders", methods=["GET"])
def account_orders():
    # Check authentication and authorisation
    auth_response = check_auth()
    if auth_response:
        return auth_response
    
    user_id = session['user_id']
    customer_id = get_customer_by_user_id(user_id)['customer_id']
    orders = get_customer_orders(customer_id)
    for order in orders:
        if 'amount' in order:
            order['amount'] = format_currency(order['amount'])

    return render_template("account_orders.html", orders=orders)

@customer.route("/account_payment_method", methods=["GET", "POST"])
def account_payment_method():
    # Check authentication and authorisation
    auth_response = check_auth()
    if auth_response:
        return auth_response
    
    #Retrive payment methods
    user_id = session['user_id']
    payment_methods = get_customer_payment_methods(user_id)
    
    #Form for adding payment method
    form = PaymentMethodForm()
    if form.validate_on_submit():
        card_type = form.card_type.data
        name_on_card = form.name_on_card.data
        expiration_month = form.expiration_month.data
        expiration_year = form.expiration_year.data
        digits = form.digits.data
        security_code = form.security_code.data

        customer_add_payment_method(user_id, card_type, name_on_card, expiration_month, expiration_year, digits, security_code)
        flash("Payment method added successfully!", "success")
        return redirect(url_for('customer.account_payment_method'))

    flash_form_errors(form)

    return render_template("account_payment_method.html", form=form, payment_methods=payment_methods)

@customer.route("/remove_payment_method", methods=["GET", "POST"])
def remove_payment_method():
    # Check authentication and authorisation
    auth_response = check_auth()
    if auth_response:
        return auth_response
    
    card_id = request.form.get('card_id')
    if card_id:
        delete_payment_method(card_id)
        flash('Payment method removed sucessfully.', 'success')

    return redirect(url_for('customer.account_payment_method'))

@customer.route("/view_order_details/<int:order_id>")
def view_order_details(order_id):
     # Check authentication and authorisation
    auth_response = check_auth()
    if auth_response:
        return auth_response
    
    bookings = get_booking_info_by_order_id(order_id)
    order = get_order_by_order_id(order_id)
    total_shipping_price = sum(booking['shipping_price'] for booking in bookings)
    invoice_subtotal = sum(booking['amount'] for booking in bookings)

    return render_template("customer_view_order_details.html", bookings=bookings, order=order, total_shipping_price=total_shipping_price, invoice_subtotal=invoice_subtotal)

@customer.route("/order_cancellation/<int:order_id>", methods=["POST"])
def order_cancellation(order_id):
     # Check authentication and authorisation
    auth_response = check_auth()
    if auth_response:
        return auth_response
    
    try:
        result = cancel_order(order_id)
        if result:
            flash(result, "danger")  # Handle the return message from cancel_order
        else:
            flash("Order and associated bookings cancelled successfully.", "success")
    except Exception as e:
        flash(f"Failed to cancel order: Please contact our staff to arrange cancellation. Error: {e}", "danger")
    
    return redirect(url_for('customer.account_orders'))

@customer.route("/enquiry", methods=["GET", "POST"])
def enquiry():
    form = enquiryForm()
    customer = get_customer_by_user_id(session['user_id'])
    stores = get_all_stores_list()
    form.store.choices = [(store, store) for store in stores]

    if form.validate_on_submit():
        store = form.store.data
        subject = form.subject.data
        message_text = form.message_text.data
        
        add_messsage(customer['user_id'], store, subject, message_text)
        flash("Message sent successfully.", "success")
        return redirect(url_for('customer.enquiry'))
    else:
        form.customer.data = customer['customer_id']
        form.firstname.data = customer['first_name']
        form.lastname.data = customer['last_name']
    return render_template("enquiry.html", form=form)

@customer.route("/notification", methods=["GET", "POST"])
def notification():
    auth_response = check_auth()
    if auth_response:
        return auth_response

    return render_template("account_notification.html")
