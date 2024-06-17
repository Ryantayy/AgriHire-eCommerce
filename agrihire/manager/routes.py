from flask import Blueprint, render_template, flash, redirect, url_for, session, request,make_response,jsonify
import re
import os
from agrihire.auth.routes import check_password
from agrihire.manager.forms import EditManagerProfileForm, addStaffForm, changePasswordForm, editStaffForm, addPromotionForm, editPromotionForm,EditEquipmentForm,RequestServiceForEquipmentForm, StoreForm, createNotificationForm,MgrEquipmentRetireForm
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename

from agrihire.utilities import add_staff, deactive_staff_by_user_id, get_all_staffs, get_all_staffs_by_store_id, get_all_stores_list, get_manager_by_user_id, get_staff_details_by_user_id, get_store_id_by_user_id, get_store_name_by_id, get_user_by_email, get_user_titles, hash_password, reset_password, update_manager_profile, update_staff,get_total_income,get_total_expense,get_total_income_for_store,get_total_expense_for_store,get_customers_count,get_orders_count,get_income_by_month,get_expense_by_month,get_promotion_by_promotion_id, update_promotion, remove_promotion,add_Image,get_all_sub_category_details,get_all_promotions,add_promotion_item,get_total_expense_for_store_by_month,get_total_income_for_store_by_month,get_shipping_count,get_shipping_count_by_store,get_booking_amount,get_booking_amount_by_store,get_orders_by_store,get_customer_by_store,get_store_id_by_staff_user_id,get_all_equipments_by_store_id,get_all_equipments,get_equipment_details_by_id,Update_equipment_condition,add_service_for_equipment,add_store_function,get_store_by_id,update_store,get_all_stores_with_managers,get_available_equipment_by_store,get_all_available_equipment,get_all_orders,get_all_orders_by_store,get_local_manager, retrieve_all_notifications, generate_notification, remove_notification, get_all_customer,update_equipment_status
import pdfkit
from agrihire import app

manager = Blueprint("manager", __name__, template_folder="templates")

# region functions

@manager.context_processor
def inject_inconme():
    if session['role_id'] == 3:
        store_id = get_store_id_by_user_id(session['user_id'])
        
        #getting values for local manager
        total_income = get_total_income_for_store(store_id['store_id'])
        total_expense = get_total_expense_for_store(store_id['store_id'])
        
        if total_income['total_amount'] is None:
               total_income_amount = 0
        else:
               total_income_amount = total_income['total_amount']

        if total_expense['total_expense'] is None:
               total_expense_amount = 0
        else:
               total_expense_amount = total_expense['total_expense']
               
        profit = total_income_amount - total_expense_amount
    else:
        #getting values for national manager
        total_income = get_total_income()
        total_expense = get_total_expense()
        
        if total_income is None:
               total_income_amount = 0
        else:
               total_income_amount = total_income['total_amount']

        if total_expense is None:
               total_expense_amount = 0
        else:
               total_expense_amount = total_expense['total_expense']
               
        profit = total_income_amount - total_expense_amount
    return dict(total_income = total_income_amount, total_expense = total_expense_amount, profit=profit)

def format_timedelta(delta):
    # A datetime object for midnight of a given day
    midnight = datetime.combine(datetime.today(), datetime.min.time())
    # Add the timedelta to midnight to get a datetime object
    datetime_with_delta = midnight + delta
    # Extract the time component
    time = datetime_with_delta.time()
    return time


def flash_form_errors(form):
    if form.errors:
        for error_messages in form.errors.values():
            for error in error_messages:
                flash(f"{error}", "danger")


def check_auth():
    if not 'loggedin' in session:
        flash("Please login first.", "danger")
        return redirect(url_for('auth.login'))

    if session['role_id'] != 3 and session['role_id'] !=5:
        flash("Invalid action! Back to home page.", "danger")
        return redirect(url_for('main.home'))
    return None

@manager.route("/dashboard", methods=["GET"])
def dashboard():
    # Check authentication and authorisation
    auth_response = check_auth()
    if auth_response:
        return auth_response
    
    if session['role_id'] == 5:
    
          customer_count = get_customers_count()
          if customer_count['customer_count'] is None:
                  customer_count['customer_count'] = 0

          orders_count = get_orders_count()
          if orders_count['orders_count'] is None:
                  orders_count['orders_count'] = 0

          income_by_month = get_income_by_month()      

          expense_by_month = get_expense_by_month()

          shipping_count = get_shipping_count()
          if shipping_count['shipping_count'] is None:
                  shipping_count['shipping_count'] = 0
                  
          shipping_cost = 150 * shipping_count['shipping_count']
          
          booking_amount = get_booking_amount()
          if booking_amount['booking_amount'] is None:
                      booking_amount['booking_amount'] = 0
    else:
       store_id = get_store_id_by_user_id(session['user_id'])
       
       customer_count = get_customer_by_store(store_id['store_id'])
       if customer_count['customer_count'] is None:
                  customer_count['customer_count'] = 0
                  
       orders_count = get_orders_by_store(store_id['store_id'])
       if orders_count['orders_count'] is None:
                  orders_count['orders_count'] = 0
       
       income_by_month = get_total_income_for_store_by_month(store_id['store_id'])
                  
       expense_by_month = get_total_expense_for_store_by_month(store_id['store_id'])
     
                  
       shipping_count = get_shipping_count_by_store(store_id['store_id'])
       if shipping_count['shipping_count'] is None:
                shipping_count['shipping_count'] = 0
        
       shipping_cost = 150 * shipping_count['shipping_count']
       
       booking_amount = get_booking_amount_by_store(store_id['store_id'])
       if booking_amount['booking_amount'] is None:
                booking_amount['booking_amount'] = 0
       
    return render_template("mgr_mainpage.html",customer_count = customer_count,orders_count = orders_count,income_by_month = income_by_month,expense_by_month=expense_by_month, shipping_cost = shipping_cost,booking_amount = booking_amount['booking_amount'])
 
@manager.route("/account_profile", methods=["GET", "POST"])
def account_profile():
    manager_type = -1
    if session['role_id'] == 3:
       manager_type = 0
    elif session['role_id'] == 5:
        manager_type = 1
    form = EditManagerProfileForm()
    password_form = changePasswordForm() 
    user = get_manager_by_user_id(session['user_id'], manager_type)

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
        update_manager_profile(title, firstname, lastname, email, phone, address, manager_type)
        session['email'] = email
        flash("Profile updated successfully!", "success")
        return redirect(url_for('manager.account_profile'))
    else:
        form.title.data = user['title']
        form.firstname.data = user['first_name']
        form.lastname.data = user['last_name']
        form.original_email.data = user['email']
        form.email.data = user['email']
        form.phone.data = user['phone']
        form.address.data = user['address']

    flash_form_errors(form)
    return render_template("mgr_profile.html", form=form, password_form=password_form)

@manager.route("/change_password", methods=["GET", "POST"])
def change_password():
    # Check authentication and authorisation
    auth_response = check_auth()
    if auth_response:
        return auth_response
    
    manager_type = -1
    if session['role_id'] == 3:
       manager_type = 0
    elif session['role_id'] == 5:
        manager_type = 1
    form = EditManagerProfileForm()
    user = get_manager_by_user_id(session['user_id'], manager_type)
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

        return redirect(url_for('manager.dashboard'))

    flash_form_errors(password_form)
    return render_template("mgr_profile.html", form=form, password_form=password_form)
 
@manager.route("/staffs", methods=["GET", "POST"])
def staffs():
    if session['role_id'] == 3:
        store_id = get_store_id_by_user_id(session['user_id'] )
        staffs = get_all_staffs_by_store_id(store_id["store_id"])
    else:
        staffs = get_all_staffs()
    return render_template("mgr_staffs.html", staffs=staffs)

@manager.route("/search_staff", methods=["GET"])
def search_staff():
    search_query = request.args.get('search_query')

    if session['role_id'] == 3:
        store_id = get_store_id_by_user_id(session['user_id'] )
        staffs = get_all_staffs_by_store_id(store_id["store_id"])
    else:
        staffs = get_all_staffs()

    if search_query:
       results = [staff for staff in staffs if search_query.lower() in staff['staff_name'].lower() or search_query.lower() in staff['email'].lower()]
    else:
        results = []
    return render_template("mgr_staffs.html", staffs=results)

@manager.route("/delete_staff/<int:user_id>", methods=["GET","POST"])
def delete_staff(user_id):
    try:
       deactive_staff_by_user_id(user_id)
    except:
        flash_form_errors("Something wrong during de-actived this staff.")
 
    flash("Successfully deactived this staff")
    if session['role_id'] == 3:
        store_id = get_store_id_by_user_id(session['user_id'] )
        staffs = get_all_staffs_by_store_id(store_id["store_id"])
    else:
        staffs = get_all_staffs()
    return render_template("mgr_staffs.html", staffs=staffs) 

@manager.route("/add_new_staff", methods=["GET","POST"])
def add_new_staff():
    auth_response = check_auth()
    if auth_response:
        return auth_response

    form = addStaffForm()
    user_titles = get_user_titles()
    form.title.choices = [(title, title) for title in user_titles]
    stores = get_all_stores_list()
    form.store.choices = [(store, store) for store in stores]
    
    if session['role_id'] == 3:
        store_id = get_store_id_by_user_id(session['user_id'])
        store = get_store_name_by_id (store_id["store_id"])
        if store_id:
            form.store.data = store["store_name"]
            form.store.render_kw = {'disabled': 'disabled'}
    
    if form.validate_on_submit():
        title_id = form.title.data
        email = form.email.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        phone = form.phone.data
        address = form.address.data
        store = form.store.data
        password = form.password.data
       
        add_staff(title_id, email, firstname, lastname, phone, address, store, password)
        flash("Staff added successfully.", "success")

        if session['role_id'] == 3:
            store_id = get_store_id_by_user_id(session['user_id'] )
            staffs = get_all_staffs_by_store_id(store_id["store_id"])
        else:
            staffs = get_all_staffs()
        return render_template("mgr_staffs.html", staffs=staffs)
    flash_form_errors(form)
    return render_template("mgr_add_staff.html", form=form)  
  
@manager.route("/edit_staff/<int:user_id>", methods=["GET","POST"])
def edit_staff(user_id):
    auth_response = check_auth()
    if auth_response:
        return auth_response

    form = editStaffForm()
    user_titles = get_user_titles()
    form.title.choices = [(title, title) for title in user_titles]
    stores = get_all_stores_list()
    form.store.choices = [(store, store) for store in stores]
    
    user = get_staff_details_by_user_id(user_id)
    
    if session['role_id'] == 3:
        store_id = get_store_id_by_user_id(session['user_id'])
        store = get_store_name_by_id (store_id["store_id"])
        if store_id:
            form.store.data = store["store_name"]
            form.store.render_kw = {'disabled': 'disabled'}
    
    if form.validate_on_submit():
        title_id = form.title.data
        email = form.email.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        phone = form.phone.data
        address = form.address.data
        store = form.store.data
        # password = form.password.data
       
        update_staff(user_id,title_id, email, firstname, lastname, phone, address, store)
        flash("Staff updated successfully.", "success")

        if session['role_id'] == 3:
            store_id = get_store_id_by_user_id(session['user_id'] )
            staffs = get_all_staffs_by_store_id(store_id["store_id"])
        else:
            staffs = get_all_staffs()
        return render_template("mgr_staffs.html", staffs=staffs)
    else:
        form.title.data = user['title']
        form.firstname.data = user['first_name']
        form.lastname.data = user['last_name']
        form.email.data = user['email']
        form.phone.data = user['phone']
        form.address.data = user['address']
        form.original_email.data = user['email']
        form.store.data = user["store_name"]
    
    flash_form_errors(form)
    return render_template("mgr_edit_staff.html", form=form, user_id=user_id)  

@manager.route("/search_promotion", methods=["GET", "POST"])
def search_promotion():
    search_query = request.args.get('search_query')
    sub_categories = get_all_sub_category_details()
    if search_query:
       results = [sc for sc in sub_categories if search_query.lower() in sc['sub_category_name'].lower() or search_query.lower() in sc['category_name'].lower()]
    else:
       results = []
    return render_template("nat_mgr_promotion.html", sub_categories=results)

@manager.route("/promotion", methods=["GET", "POST"])
def promotion():
    auth_response = check_auth()
    if auth_response:
        return auth_response
    
    promotions = get_all_promotions()

    return render_template("nat_mgr_promotion.html", promotions = promotions)

@manager.route("add_promotion", methods=["GET", "POST"])
def add_promotion():
    auth_response = check_auth()
    if auth_response:
        return auth_response

    form = addPromotionForm()
    sub_categories = get_all_sub_category_details()
    form.equipment.choices = [(sub_category['sub_category_id'], sub_category['sub_category_name']) for sub_category in sub_categories]

    
    if form.validate_on_submit():
        title = form.title.data
        equipment = form.equipment.data
        description = form.description.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        discount_rate = form.discount_rate.data

        image_id = None
        if form.image.data:
            image_file = form.image.data
            filename = secure_filename(image_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'promotions', filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            image_file.save(file_path)

            relative_image_url = f'{filename}'
            image_id = add_Image(sub_category_id=0, entity_id=7, entity_type='promotion', image_url=relative_image_url)

        try:
            add_promotion_item(title, equipment, image_id, description, start_date, end_date, discount_rate)
            flash("Promotion added successfully.", "success")
        except Exception as e:
            flash(f"Failed to add promotion: {str(e)}", "danger")
    
    flash_form_errors(form)
    return render_template("nat_mgr_add_promotion.html", form=form)

@manager.route("/edit_promotion/<int:promotion_id>", methods=["GET", "POST"])
def edit_promotion(promotion_id):
    auth_response = check_auth()
    if auth_response:
        return auth_response

    promotion = get_promotion_by_promotion_id(promotion_id)

    form = editPromotionForm()
    sub_categories = get_all_sub_category_details()
    form.equipment.choices = [(sub_category['sub_category_id'], sub_category['sub_category_name']) for sub_category in sub_categories]
    print(form.equipment.choices)

    if request.method == 'GET':
        form.promotion_id.data = promotion_id
        form.title.data = promotion['title']
        form.equipment.data = promotion['sub_category_id']
        form.description.data = promotion['description']
        form.start_date.data = promotion['start_date']
        form.end_date.data = promotion['end_date']
        form.discount_rate.data = int(promotion['discount_rate'])

    if form.validate_on_submit():
        title = form.title.data
        equipment = form.equipment.data
        description = form.description.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        discount_rate = form.discount_rate.data

        image_id = promotion['image_id']
        if form.image.data:
            image_file = form.image.data
            filename = secure_filename(image_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'promotions', filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            image_file.save(file_path)

            relative_image_url = f'{filename}'
            image_id = add_Image(sub_category_id=0, entity_id=7, entity_type='promotion', image_url=relative_image_url)

        try:
            update_promotion(promotion_id, title, equipment, image_id, description, start_date, end_date, discount_rate)
            flash("Promotion updated successfully.", "success")
            return redirect(url_for('manager.promotion'))
        except Exception as e:
            flash(f'Failed to update promotion: {str(e)}', 'danger')

    flash_form_errors(form)
    return render_template("nat_mgr_edit_promotion.html", form=form, promotion=promotion)


@manager.route("/delete_promotion/<int:promotion_id>", methods=["GET","POST"])
def delete_promotion(promotion_id):
    auth_response = check_auth()
    if auth_response:
        return auth_response
    
    try:
        remove_promotion(promotion_id)
    except:
        flash_form_errors("Something wrong during deleting this promotion.")
 
    flash("Successfully delete this promotion", 'success')

    return redirect(url_for('manager.promotion'))
 
@manager.route("/equipments", methods=["GET", "POST"])
def equipments():
    return render_template("mgr_equipments.html")
 
@manager.route("/orders", methods=["GET", "POST"])
def orders():
    
    auth_response = check_auth()
    if auth_response:
        return auth_response
    
    if session['role_id'] == 3:
        store_id = get_store_id_by_user_id(session['user_id'])
        orders = get_all_orders_by_store(store_id['store_id'])
    else:
        orders = get_all_orders()
    
    return render_template("mgr_orders.html",orders = orders)
 
@manager.route("/reports")
def reports():
    
    auth_response = check_auth()
    if auth_response:
        return auth_response
 
    # Rendering HTML Templates
    return render_template('mgr_reports.html')
    
 
 # for national manager
@manager.route("/local_managers", methods=["GET", "POST"])
def local_managers():
    
    auth_response = check_auth()
    if auth_response:
        return auth_response
    
    local_managers = get_local_manager()
    
    return render_template("nat_mgr_local_managers.html",local_managers = local_managers)
 
# for national manager
@manager.route("/nat_stores", methods=["GET", "POST"])
def nat_stores():
     return render_template("nat_mgr_stores.html")

@manager.route("/notification", methods=["GET", "POST"])
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
        return redirect(url_for('manager.notification'))
    
    flash_form_errors(form)
    return render_template("manager_notification.html", notifications=notifications, form=form)

@manager.route("/delete_notification/<int:notification_id>", methods=["GET", "POST"])
def delete_notification(notification_id):
    auth_response = check_auth()
    if auth_response:
        return auth_response
    
    remove_notification(notification_id)

    flash("Notification deleted successfully!", "success")
    return redirect(url_for('manager.notification'))

@manager.route('/download-pdf')
def download_pdf():
    
    auth_response = check_auth()
    if auth_response:
        return auth_response
    
    # Rendering HTML Templates
    rendered_html = render_template('mgr_reports_download.html')
    
    # Configure pdfkit and specify the path of wkhtmltopdf
    basedir = os.path.abspath(os.path.dirname(__file__))
    # Constructs the relative path to the wkhtmltopdf executable
    path_wkhtmltopdf = os.path.join(basedir, 'wkhtmltopdf', 'bin', 'wkhtmltopdf.exe')

    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    
    #Python anywhere path of wkhtmltopdf 
    #config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

    # Set options to avoid certain network errors
    options = {
        'no-outline': None,
        'disable-smart-shrinking': None,
        'quiet': '',
        'disable-external-links': '',
        'disable-internal-links': '',
        'disable-javascript': '',
        'load-error-handling': 'ignore'
    }

    try:
        # Convert HTML to PDF
        pdf = pdfkit.from_string(rendered_html, False, configuration=config, options=options)
    except IOError as e:
        error_output = e.args[0].decode('utf-8') if isinstance(e.args[0], bytes) else e.args[0]
        print("PDFKit error output:\n", error_output)
        raise e

    # Build a response to let the browser download the PDF file
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=finacial_report.pdf'
    return response

@manager.route("/equipment_condition", methods=["GET", "POST"])
def equipment_condition():
    if session['role_id'] == 3:
       store_id = get_store_id_by_user_id(session['user_id'])
       equipments = get_all_equipments_by_store_id(store_id['store_id'])
    else:
        equipments = get_all_equipments()
    return render_template("mgr_equipment_condition.html",  equipments=equipments)

@manager.route("/search", methods=["GET", "POST"])
def search(): 
    search_query = request.args.get('search_query')
    if session['role_id'] == 3:
       store_id = get_store_id_by_user_id(session['user_id'])
       equipments = get_all_equipments_by_store_id(store_id['store_id'])
       
    else:
        equipments = get_all_equipments()
        
    if search_query:
       results = [sc for sc in equipments if search_query.lower() in sc['sub_category_name'].lower() or search_query.lower() in sc['serial_number'].lower()]
    else:
       results = []
    return render_template("mgr_equipment_condition.html", equipments=results)

@manager.route("/edit_equipment_condition/<int:equipment_id>", methods=["GET", "POST"])
def edit_equipment_condition(equipment_id):
    form = EditEquipmentForm()
    equipment_details = get_equipment_details_by_id(equipment_id)
    if form.validate_on_submit():
        equipment_condition = form.equipment_condition.data

        Update_equipment_condition(equipment_id, equipment_condition)
        flash("Equipment updated successfully!", "success")
        return redirect(url_for('manager.equipment_condition'))
    else:
        form.sub_category_name.data = equipment_details['sub_category_name']
        form.serial_number.data = equipment_details['serial_number']
        form.equipment_condition.data = equipment_details['equipment_condition']
       
    flash_form_errors(form) 
    return render_template('mgr_edit_equipment_condition.html', form=form , equipment_id=equipment_id)

@manager.route("/request_service/<int:equipment_id>", methods=["GET", "POST"])
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
        return redirect(url_for('manager.equipment_condition'))
    else:
        form.equipment_id.data = equipment_id
        
    flash_form_errors(form) 
    return render_template('mgr_add_service.html', form=form , equipment_id=equipment_id)

@manager.route("/stores/add", methods=['GET', 'POST'])
def add_store():
    form = StoreForm()

    if form.validate_on_submit():
        store_name = form.store_name.data
        address = form.address.data

        image_id = None
        if form.image.data:
            image_file = form.image.data
            filename = secure_filename(image_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'stores-logo', filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            image_file.save(file_path)

            relative_image_url = f'{filename}'
            image_id = add_Image(sub_category_id=0, entity_id=6, entity_type='store', image_url=relative_image_url)

        try:
            add_store_function(store_name, address, image_id)
            flash("New store added successfully!", "success")
            return redirect(url_for('manager.stores'))
        except Exception as e:
            flash(f"Failed to add store: {str(e)}", "danger")

    return render_template("mgr_add_store.html", form=form)


@manager.route('/stores/edit/<int:store_id>', methods=['GET', 'POST'])
def edit_store(store_id):
    store = get_store_by_id(store_id)
    if not store:
        flash('Store not found!', 'danger')
        return redirect(url_for('manager.stores'))
    
    form = StoreForm(obj=store)
    
    if form.validate_on_submit():
        store_name = form.store_name.data
        address = form.address.data
        image_file = form.image.data
        
        image_id = store.get('image_id')

        if image_file:
            filename = secure_filename(image_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'stores-logo', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            image_file.save(filepath)

            image_id = add_Image(sub_category_id=0, entity_id=6, entity_type='store', image_url=filename)

        try:
            update_store(store_id, store_name, address, image_id)
            flash('Store updated successfully!', 'success')
            return redirect(url_for('manager.stores'))
        except Exception as e:
            flash(f'Failed to update store: {e}', 'danger')
    
    return render_template('mgr_edit_store.html', form=form, store=store)

# for national manager
@manager.route("/stores", methods=["GET"])
def stores(): 
    if check_auth():
        return check_auth()
    stores = get_all_stores_with_managers()  # Fetch data using a utility function
    return render_template("mgr_stores.html", stores=stores)

@manager.route("/inventory")
def inventory(): 
    if check_auth():
        return check_auth()
    
    if session['role_id'] == 3:
        store_id = get_store_id_by_user_id(session['user_id']) 
        inventory = get_available_equipment_by_store(store_id['store_id'])  
    else:
        inventory = get_all_available_equipment()     
    
    return render_template("mgr_inventory.html", inventory=inventory)

@manager.route("/retire_equipment/<int:equipment_id>", methods=["GET", "POST"])
def retire_equipment(equipment_id):
    
    if check_auth():
        return check_auth()
       
    form = MgrEquipmentRetireForm()
    form.equipment_id.data = equipment_id
    if form.validate_on_submit():
        retire_date = form.retire_date.data
        update_equipment_status(equipment_id)
        flash("Equipment service requested successfully!", "success")
        return redirect(url_for('manager.equipment_condition'))
    else:
        form.equipment_id.data = equipment_id
    flash_form_errors(form) 
    return render_template('mgr_retire_equipment.html', form=form , equipment_id=equipment_id)