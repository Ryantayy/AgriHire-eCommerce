from flask import Blueprint, render_template, flash, redirect, url_for, session, request

from datetime import datetime, timedelta
from agrihire.auth.routes import check_password
from agrihire.customer.forms import EditCustomerProfileForm
from agrihire.dbconnection import getCursor

from agrihire.staff.forms import EditEquipmentForm, EditStaffProfileForm, EquipmentRetireForm, editEnquiryForm, createNotificationForm, RequestServiceForEquipmentForm, editEnquiryForm
from agrihire.staff.forms import changePasswordForm
from agrihire.utilities import  Update_equipment_condition, cancel_order_and_bookings, get_all_equipments, get_all_orders, get_all_orders_by_store, get_all_stores_list, get_booking_info_by_order_id, get_customer_by_user_id, get_equipment_details_by_id, get_message_by_id, get_message_by_store_id, get_order_by_order_id, get_orders_info_for_this_week, get_orders_info_for_today_pickup, get_orders_info_for_today_shipping,  get_staff_by_user_id, get_store_id_by_staff_user_id, get_store_id_by_user_id, get_user_by_email, get_user_titles, hash_password, reset_password, update_equipment_status, update_message_read_status, update_message_table_with_reply, update_staff_profile, retrieve_all_notifications, get_all_customer, generate_notification, remove_notification,get_all_equipments_by_store_id,add_service_for_equipment,get_services_by_store_id

staff = Blueprint("staff", __name__, template_folder="templates")

# region functions

def check_auth():
    if not 'loggedin' in session:
        flash("Please login first.", "danger")
        return redirect(url_for('auth.login'))

    if session['role_id'] != 2:
        flash("Invalid action! Back to home page.", "danger")
        return redirect(url_for('main.home'))
    return None


def flash_form_errors(form):
    if form.errors:
        for error_messages in form.errors.values():
            for error in error_messages:
                flash(f"{error}", "danger")


def format_timedelta(delta):
    # A datetime object for midnight of a given day
    midnight = datetime.combine(datetime.today(), datetime.min.time())
    # Add the timedelta to midnight to get a datetime object
    datetime_with_delta = midnight + delta
    # Extract the time component
    time = datetime_with_delta.time()
    return time

# endregion

# region routes

@staff.route("/dashboard", methods=["GET"])
def dashboard():
    # Check authentication and authorisation
    auth_response = check_auth()
    if auth_response:
        return auth_response

    store_id = get_store_id_by_staff_user_id(session['user_id'])
   
    orders_for_today_pickup = get_orders_info_for_today_pickup(store_id['store_id'])
    orders_for_today_shipping = get_orders_info_for_today_shipping(store_id['store_id'])
    orders_for_this_week = get_orders_info_for_this_week(store_id['store_id'])

    return render_template("main_dashboard.html", orders_for_today_pickup=orders_for_today_pickup, orders_for_today_shipping=orders_for_today_shipping, orders_for_this_week=orders_for_this_week)

@staff.route("/staff_account_settings", methods=["GET", "POST"])
def staff_account_settings():
    form = EditStaffProfileForm()
    password_form = changePasswordForm() 
    user = get_staff_by_user_id(session['user_id'])

    user_titles = get_user_titles()
    form.title.choices = [(title, title) for title in user_titles]

    if form.validate_on_submit():
        title = form.title.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        phone = form.phone.data
        address = form.address.data

        # Update the user profile
        update_staff_profile(title, firstname, lastname, email, phone, address)
        session['email'] = email
        flash("Profile updated successfully!", "success")
        return redirect(url_for('staff.staff_account_settings'))
    else:
        form.title.data = user['title']
        form.firstname.data = user['first_name']
        form.lastname.data = user['last_name']
        form.original_email.data = user['email']
        form.email.data = user['email']
        form.phone.data = user['phone']
        form.address.data = user['address']

    flash_form_errors(form)
    return render_template("staff_account_settings.html", form=form, password_form=password_form)

@staff.route("/change_password", methods=["GET", "POST"])
def change_password():
    # Check authentication and authorisation
    auth_response = check_auth()
    if auth_response:
        return auth_response

    #Retrieve user details
    form = EditStaffProfileForm()
    user = get_staff_by_user_id(session['user_id'])
    user_titles = get_user_titles()
    form.title.choices = [(title, title) for title in user_titles]

    form.title.data = user['title']
    form.firstname.data = user['first_name']
    form.lastname.data = user['last_name']
    form.original_email.data = user['email']
    form.email.data = user['email']
    form.phone.data = user['phone']
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

        return redirect(url_for('staff.dashboard'))

    flash_form_errors(password_form)
    return render_template("staff_account_settings.html", form=form, password_form=password_form)

@staff.route("/view_customer_profile/<int:user_id>", methods=["GET"])
def view_customer_profile(user_id):
    form = EditCustomerProfileForm()
    user = get_customer_by_user_id(user_id)

    user_titles = get_user_titles()
    form.title.choices = [(title, title) for title in user_titles]

    form.title.data = user['title']
    form.firstname.data = user['first_name']
    form.lastname.data = user['last_name']
    form.original_email.data = user['email']
    form.email.data = user['email']
    form.phone.data = user['phone']
    form.address.data = user['address']

    return render_template("view_customer_profile.html", form=form)

@staff.route("/equipment_condition", methods=["GET", "POST"])
def equipment_condition():
    store_id = get_store_id_by_staff_user_id(session['user_id'])
    equipments = get_all_equipments_by_store_id(store_id['store_id'])
    return render_template("equipment_condition.html",  equipments=equipments)

@staff.route("/search", methods=["GET", "POST"])
def search():
    search_query = request.args.get('search_query')
    store_id = get_store_id_by_staff_user_id(session['user_id'])
    equipments = get_all_equipments_by_store_id(store_id['store_id'])
    if search_query:
       results = [sc for sc in equipments if search_query.lower() in sc['sub_category_name'].lower() or search_query.lower() in sc['serial_number'].lower()]
    else:
       results = []
    return render_template("equipment_condition.html", equipments=results)

@staff.route("/edit_equipment_condition/<int:equipment_id>", methods=["GET", "POST"])
def edit_equipment_condition(equipment_id):
    form = EditEquipmentForm()
    equipment_details = get_equipment_details_by_id(equipment_id)
    if form.validate_on_submit():
        equipment_condition = form.equipment_condition.data

        Update_equipment_condition(equipment_id, equipment_condition)
        flash("Equipment updated successfully!", "success")
        return redirect(url_for('staff.equipment_condition'))
    else:
        form.sub_category_name.data = equipment_details['sub_category_name']
        form.serial_number.data = equipment_details['serial_number']
        form.equipment_condition.data = equipment_details['equipment_condition']
       
    flash_form_errors(form) 
    return render_template('edit_equipment_condition.html', form=form , equipment_id=equipment_id)

@staff.route("/booking_history", methods=["GET", "POST"])
def booking_history():
    store_id = get_store_id_by_staff_user_id(session['user_id'])
    orders = get_all_orders_by_store(store_id['store_id'])
    return render_template("booking_history.html", orders=orders)

@staff.route("/view_order_details/<int:order_id>", methods=["GET"])
def view_order_details(order_id):
    bookings = get_booking_info_by_order_id(order_id)
    order = get_order_by_order_id(order_id)
    total_shipping_price = sum(booking['shipping_price'] for booking in bookings)
    subtotal = sum(booking['amount'] for booking in bookings)

    return render_template("view_order_details.html", bookings=bookings, order=order, total_shipping_price=total_shipping_price, subtotal=subtotal)

@staff.route("/search_order", methods=["GET"])
def search_order():
    search_query = request.args.get('search_query')
    store_id = get_store_id_by_staff_user_id(session['user_id'])
    orders = get_all_orders_by_store(store_id['store_id'])
    if search_query:
       results = [order for order in orders if search_query.lower() in order['customer_name'].lower() or search_query in str(order['order_id'])]
    else:
        results = []
    return render_template("booking_history.html", orders=results)

@staff.route("/cancel_order/<int:order_id>", methods=["GET", "POST"])
def cancel_order(order_id):
    cancel_order_and_bookings(order_id)
    store_id = get_store_id_by_staff_user_id(session['user_id'])
    orders = get_all_orders_by_store(store_id['store_id'])
    return render_template("booking_history.html", orders=orders)

@staff.route("/message", methods=["GET", "POST"])
def message():
    store_id = get_store_id_by_staff_user_id(session['user_id'])

    messages = get_message_by_store_id(store_id['store_id'])
    return render_template("message.html",messages=messages)

@staff.route("/search_message", methods=["GET"])
def search_message():
    search_query = request.args.get('search_query')
    store_id = get_store_id_by_staff_user_id(session['user_id'])

    messages = get_message_by_store_id(store_id['store_id'])
    if search_query:
       results = [message for message in messages if search_query.lower() in message['subject'].lower() 
       or search_query in str(message['message_id']) 
       or search_query.lower() in message['customer_name'].lower() ]
    else:
      results = []

    return render_template("message.html",messages=results)

@staff.route("/edit_message/<int:message_id>", methods=["GET", "POST"])
def edit_message(message_id):
    #send_id and receiver_id are all user_id 
    form = editEnquiryForm()
    message_detail = get_message_by_id(message_id)
    customer = get_customer_by_user_id(message_detail["sender_id"])
    store_id = get_store_id_by_staff_user_id(session['user_id'])
   
    if form.validate_on_submit():
        body_message =  form.reply_text.data
        update_message_table_with_reply(message_id, session['user_id'], message_detail["sender_id"], store_id['store_id'], message_detail['subject'], body_message, message_id )
        return redirect('mailto:' + customer['email'] + '?subject=Replay ' + message_detail['subject'] + '?body= ' + body_message)
    else:
        form.customer.data = customer['customer_id']
        form.firstname.data = customer['first_name']
        form.lastname.data = customer['last_name']
        form.email.data = customer['email']
        form.subject.data = message_detail['subject']
        form.message_text.data = message_detail['message_text']
   
    return render_template("edit_message.html", form=form, customer=customer , message_detail=message_detail,message_id=message_id)

@staff.route('/update_message_status/<int:message_id>', methods=['POST'])
def update_message_status(message_id):
    message_detail = get_message_by_id(message_id)
    if message_detail["status"] != "responded":
        return update_message_read_status(message_id) 

@staff.route("/notification", methods=["GET", "POST"])
def notification():
    auth_response = check_auth()
    if auth_response:
        return auth_response

    notifications = retrieve_all_notifications()

    form = createNotificationForm()
    customers = get_all_customer()
    form.recipient.choices = [('', 'All Customers')]  # Add an option for all customers
    form.recipient.choices += [(customer['user_id'], customer['full_name']) for customer in customers]

    if form.validate_on_submit():
        user_id = form.recipient.data
        message = form.message.data
        
        generate_notification(user_id, message)
        flash("Notification created successfully!", "success")
        return redirect(url_for('staff.notification'))
    
    flash_form_errors(form)
    return render_template("notification.html", notifications=notifications, form=form)

@staff.route("/delete_notification/<int:notification_id>", methods=["GET", "POST"])
def delete_notification(notification_id):
    auth_response = check_auth()
    if auth_response:
        return auth_response
    
    remove_notification(notification_id)

    flash("Notification deleted successfully!", "success")
    return redirect(url_for('staff.notification'))
    
@staff.route("/request_service/<int:equipment_id>", methods=["GET", "POST"])
def request_service(equipment_id):
    
    form = RequestServiceForEquipmentForm()
    form.equipment_id.data = equipment_id
    if form.validate_on_submit():
        service_date = form.service_date.data
        cost = form.cost.data
        description = form.description.data

        add_service_for_equipment(equipment_id, service_date, cost, description)
        Update_equipment_condition(equipment_id, 'out_of_service')
        flash("Equipment service requested successfully!", "success")
        return redirect(url_for('staff.equipment_condition'))
    else:
        form.equipment_id.data = equipment_id
        
    flash_form_errors(form) 
    return render_template('add_service.html', form=form , equipment_id=equipment_id)

@staff.route("/view_equipment_service_records")
def view_equipment_service_records():
    store_id = get_store_id_by_staff_user_id(session['user_id'])
    services = get_services_by_store_id(store_id['store_id'])
    return render_template("view_equipment_service_records.html",  services=services)

@staff.route("/search_services", methods=["GET"])
def search_services():
    search_query = request.args.get('search_query')
    store_id = get_store_id_by_staff_user_id(session['user_id'])

    services = get_services_by_store_id(store_id['store_id'])
    if search_query:
       results = [service for service in services if search_query.lower() in service['description'].lower()
       or search_query in str(service['service_id']) 
       or search_query in str(service['equipment_id']) ]
    else:
      results = []

    return render_template("view_equipment_service_records.html",  services=results)

@staff.route("/retire_equipment/<int:equipment_id>", methods=["GET", "POST"])
def retire_equipment(equipment_id):
    
    form = EquipmentRetireForm()
    form.equipment_id.data = equipment_id
    if form.validate_on_submit():
        retire_date = form.retire_date.data
        update_equipment_status(equipment_id)
        flash("Equipment retired successfully!", "success")
        return redirect(url_for('staff.equipment_condition'))
    else:
        form.equipment_id.data = equipment_id
    flash_form_errors(form) 
    return render_template('retire_equipment.html', form=form , equipment_id=equipment_id)


# endregion