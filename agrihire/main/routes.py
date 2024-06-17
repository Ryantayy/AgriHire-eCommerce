from flask import Blueprint, render_template, flash, redirect, url_for, session
from flask import request, jsonify
from agrihire.main.forms import StoresForm, hireEquipmentForm, CheckoutForm, addProductForm
from decimal import Decimal
import os
from agrihire import app
from werkzeug.utils import secure_filename
from agrihire.utilities import get_all_category, get_all_equipment_overall_details, get_all_stores, get_category_name_by_category_id, get_equipment_details_by_sub_category_id, get_equipments_by_category_id, get_store_list, add_hire_booking_to_cart, get_shop_cart_items, get_hire_cost, calculate_subtotals, delete_cart_item, get_display_rates, get_available_equipment, is_equipment_in_cart, get_stores_with_available_equipment, get_customer_by_user_id, get_customer_payment_methods, customer_add_payment_method, get_sub_category_by_category,add_Image,add_products,count_num_of_product,update_equipment_stock,is_equipment_stock_from_store,add_equipment_stock, process_booking, check_booking_availability, create_order, link_order_booking, parse_datetime, parse_currency, search_database, fetch_all_news, fetch_promotions, get_discounted_equipment, retrieve_notifications,get_store_name_by_id,get_store_id_by_staff_user_id,get_store_id_by_user_id

main = Blueprint('main', __name__, template_folder='templates')

#getting data for the menu
@main.context_processor
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

@main.route("/")
@main.route("/home")
@main.route("/index")
@main.route("/default")
def home():
    promotions = fetch_promotions()
    discounted_equipments = get_discounted_equipment()
    stores = get_all_stores()[:3]
    news_items = fetch_all_news()[:4]
    return render_template("home.html", promotions=promotions,discounted_equipments=discounted_equipments,stores=stores,news_items=news_items,is_home=True)

@main.route('/about')
def about():
    return render_template('about_us.html')

@main.route('/news')
def news():
    news_items = fetch_all_news()
    main_news = news_items[0] if news_items else None
    other_news = news_items[1:4] if len(news_items) > 1 else []
    return render_template('news.html', main_news=main_news, other_news=other_news)

@main.context_processor
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

def flash_form_errors(form):
    if form.errors:
        for error_messages in form.errors.values():
            for error in error_messages:
                flash(f"{error}", "danger")

def check_auth():
    if not 'loggedin' in session:
        flash("Please login first.", "danger")
        return redirect(url_for('auth.login'))

    if session['role_id'] != 1:
        flash("Invalid action! Back to home page.", "danger")
        return redirect(url_for('main.home'))
    return None

def check_auth_without_cus():
    if not 'loggedin' in session:
        flash("Please login first.", "danger")
        return redirect(url_for('auth.login'))

    if session['role_id'] == 1:
        flash("Invalid action! Back to home page.", "danger")
        return redirect(url_for('main.home'))
    return None

@main.route('/search')
def search():
    query = request.args.get('query', '')  # Provide a default value of an empty string
    results = search_database(query)
    return render_template('search_dropdown_results.html', results=results)


@main.route("/shopitems/<int:category_id>", methods=['GET', 'POST'])
def shop_items(category_id):
    equipments = get_all_equipment_overall_details(category_id)
    category_name = get_category_name_by_category_id(category_id)
    categories = get_all_category()
    stories = get_all_stores()
    equipment_count = len(equipments)
    category_equipment_map = {}
    for category in categories:
        equipment = get_equipments_by_category_id(category['category_id'])
        category_equipment_map[category['category_id']] = equipment

    return render_template("shop_items.html", category_name=category_name, equipments=equipments, categories=categories, category_equipment_map=category_equipment_map, stories=stories, equipment_count=equipment_count,category_id=category_id )

@main.route("/shopsingleitem/<int:sub_category_id>", methods=['GET', 'POST'])
def shop_single_item(sub_category_id):
    #Retrive equipment details
    equipment_details = get_equipment_details_by_sub_category_id(sub_category_id)
    hire_rate, discounted_rate, discount_rate = get_display_rates(sub_category_id)

    # Form for booking equipment
    form = hireEquipmentForm()

    #Retrieve Store List
    store_list = get_stores_with_available_equipment(sub_category_id)
    form.sub_category_id.data = sub_category_id
    form.store.choices = [(store['store_id'], store['store_name']) for store in store_list]
    
    if form.validate_on_submit():
        #Retrive user details
        user_id = session.get('user_id')
        if not user_id:
                flash('You must be logged in to make a booking.', 'danger')
                return render_template("shop_single_item.html", equipment_details=equipment_details, sub_category_id=sub_category_id, form=form)
        # Retrieve date range from form
        store_id = int(form.store.data)
        start_datetime = form.start_datetime.data
        end_datetime = form.end_datetime.data
        
        # Check availability of equipment before form validation
        available_equipment_details = get_available_equipment(sub_category_id, store_id, start_datetime, end_datetime, user_id)
        if available_equipment_details:
            # Set equipment ID for use in subsequent validations and booking
            form.equipment_id.data = available_equipment_details['equipment_id']
            equipment_id = form.equipment_id.data

            # Process booking with confirmed availability and valid form inputs
            duration_hours = (end_datetime - start_datetime).total_seconds() / 3600
            total_cost = duration_hours * float(available_equipment_details['hire_cost'])
            add_hire_booking_to_cart(user_id, available_equipment_details['equipment_id'], start_datetime, end_datetime, total_cost)
            flash(f"{available_equipment_details['name']} has been added to your cart.", "success")
        else:
            flash("All available equipment in this category is either booked or already in your cart for the selected dates.", "danger")

        return redirect(url_for('main.shop_single_item', sub_category_id=sub_category_id))
    
    flash_form_errors(form)
    return render_template("shop_single_item.html", equipment_details=equipment_details, sub_category_id=sub_category_id, hire_rate=hire_rate, discounted_rate=discounted_rate, discount_rate=discount_rate, form=form)

@main.route("/shopcart", methods=['GET', 'POST'])
def shop_cart():
    # Check authentication and authorisation
    auth_response = check_auth()
    if auth_response:
        return auth_response
    
    user_id = session.get('user_id')
    shop_cart_items = get_shop_cart_items(user_id)
    item_subtotal, gst, subtotal, shipping_total = calculate_subtotals(shop_cart_items)

    return render_template("shop_cart.html", shop_cart_items=shop_cart_items, item_subtotal=item_subtotal, gst=gst, subtotal=subtotal)

@main.route("/shop_checkout", methods=['GET', 'POST'])
def shop_checkout():
    # Check authentication and authorisation
    auth_response = check_auth()
    if auth_response:
        return auth_response
    
    user_id = session.get('user_id')

    #Retrieve cart items
    shop_cart_items = get_shop_cart_items(user_id)
    item_subtotal, gst, subtotal, shipping_total = calculate_subtotals(shop_cart_items)

    #Retrieve User Account Details
    user_details = get_customer_by_user_id(user_id)
    payment_methods = get_customer_payment_methods(user_id)

     # Initialize the checkout form
    form = CheckoutForm()

    if form.validate_on_submit():
        #Extract form data
        address_type = form.address_type.data
        

        if address_type == 'home':
            shipping_address = user_details['address']  # Assuming the home address is stored in user_details
            include_shipping = True
        elif address_type == 'shipping':
            shipping_address = form.shipping_address.data
            include_shipping = True
        else: 
            shipping_address = "Self-Pickup"
            include_shipping = False

        special_instructions = form.special_instructions.data if form.special_instructions.data else 'None'

        # Handle payment details 
        card_type = form.card_type.data
        digits = form.digits.data
        expiration_month = form.expiration_month.data
        expiration_year = form.expiration_year.data
        security_code = form.security_code.data
        name_on_card = form.name_on_card.data
        
        customer_add_payment_method(user_id, card_type, name_on_card, expiration_month, expiration_year, digits, security_code)
        
        # Process payment and booking
        all_available = True
        store_orders = {}  # Dictionary to hold orders for each store

        for item in shop_cart_items:
            item['checkout_datetime'] = parse_datetime(item['checkout_datetime'])
            item['return_datetime'] = parse_datetime(item['return_datetime'])
            if not check_booking_availability(item['equipment_id'], item['checkout_datetime'], item['return_datetime']):
                checkout_str = item['checkout_datetime'].strftime('%Y-%m-%d %H:%M')
                return_str = item['return_datetime'].strftime('%Y-%m-%d %H:%M')
                flash('Booking conflict for item: ' + item['name'] + ' (' + checkout_str + ' - ' + return_str + ')' + '. Please remove item from cart before proceeding.', 'danger')
                all_available = False
                break  # Exit loop if any item is not available

            store_id = item['store_id']
            if store_id not in store_orders:
                store_orders[store_id] = {
                    'items': [],
                    'subtotal': Decimal('0.00'),
                    'shipping_total': Decimal('0.00')
                }
            
            store_orders[store_id]['items'].append(item)
            store_orders[store_id]['subtotal'] += parse_currency(item['total_cost'])
            store_orders[store_id]['shipping_total'] += (item['shipping_price'])

        if all_available:
            for store_id, order in store_orders.items():
                if include_shipping:
                    order_subtotal = order['subtotal'] + order['shipping_total']
                else:
                    order_subtotal = order['subtotal']
                
                # Create one order for each store
                order_id = create_order(shipping_address, special_instructions, user_details['customer_id'], order_subtotal, user_id)

                # Process each booking and link to the created order
                for item in order['items']:
                    booking_id = process_booking(user_id, item['equipment_id'], item['checkout_datetime'], item['return_datetime'], parse_currency(item['total_cost']))
                    link_order_booking(order_id, booking_id)

            flash('All bookings confirmed and order(s) created.', 'success')
            return redirect(url_for('customer.account_orders'))

    flash_form_errors(form)
    return render_template("shop_checkout.html", shop_cart_items=shop_cart_items, item_subtotal=item_subtotal, gst=gst, subtotal=subtotal, user_details=user_details,           payment_methods=payment_methods, form=form)

@main.route('/delete_cart_item/<int:cart_id>', methods=['GET', 'POST'])
def delete_cart_item_route(cart_id):
    delete_cart_item(cart_id)
    flash('Item successfully removed from cart.', 'success')
    return redirect(url_for('main.shop_cart'))

# getting sub_category accourding to the category
@main.route('/get_subcategories', methods=['GET'])
def get_subcategories():
    category_id = request.args.get('category_id')
    sub_categories = get_sub_category_by_category(category_id)
    return jsonify({'sub_categories': sub_categories})

@main.route("/add_product", methods=["GET", "POST"])
def add_product():
    # Check authentication and authorisation
    auth_response = check_auth_without_cus()
    if auth_response:
        return auth_response
    
    form = addProductForm()
    
    #Staff can only add products for their own store
    if session['role_id'] == 2:
        store_id = get_store_id_by_staff_user_id(session['user_id'])
        store_name = get_store_name_by_id(store_id['store_id'])
        form.store.choices = [(store_id['store_id'], store_name['store_name'])]
    #Local Manager can only add products for their own store
    elif session['role_id'] == 3:
        store_id = get_store_id_by_user_id(session['user_id'])
        store_name = get_store_name_by_id(store_id['store_id'])
        form.store.choices = [(store_id['store_id'], store_name['store_name'])]
    else:
       store_list = get_store_list()
       form.store.choices = [(store['store_id'], store['store_name']) for store in store_list]
    
    category_list = get_all_category()
    form.category.choices = [(category['category_id'], category['category_name']) for category in category_list]
    
    # Pre-populate subcategory choices based on initial category value
    initial_category_id = form.category.data
    sub_category_list = get_sub_category_by_category(initial_category_id)
    form.sub_category.choices = [(sub_category['sub_category_id'], sub_category['sub_category_name']) for sub_category in sub_category_list]
    
    if form.is_submitted() and form.validate():
        quantity = form.quantity.data
        store_id = form.store.data
        category_id = form.category.data
        sub_category_id = form.sub_category.data
        purchase_date = form.purchase_date.data
        purchase_cost = form.purchase_cost.data
        
        equipment_condition = form.equipment_condition.data
        equipment_status = form.equipment_status.data
        
        # product name
        category_name = next((category['category_name'] for category in category_list if category['category_id'] == int(category_id)), None)
        sub_category_name = next((sub_category['sub_category_name'] for sub_category in sub_category_list if sub_category['sub_category_id'] == int(sub_category_id)), None)
        product_name = f"{category_name} - {sub_category_name}"
        
        # adding multiple products
        for count in range(quantity):
           # serial number
           equipment_num = int(count_num_of_product()['count'])
           serial_number = f"SN{category_id}{sub_category_id}{store_id}{equipment_num +1}"
    
           add_products(product_name, serial_number, category_id, sub_category_id, store_id, purchase_date, purchase_cost,equipment_condition, equipment_status)
       
        # Determine whether there is stock
        stock = is_equipment_stock_from_store(sub_category_id,store_id)
        if stock and equipment_status == 'available':
           # update available_quantity 
           update_equipment_stock(quantity,sub_category_id)
        elif equipment_status == 'available':
            # add available_quantity
            add_equipment_stock(store_id,sub_category_id,quantity)
        
        flash("Product added successfully!", "success")
        return redirect(url_for('main.home'))
      
    flash_form_errors(form)      
    return render_template("add_product.html", form=form)


@main.route("/stores")
def stores():
    try:
        store_data = get_all_stores()
        return render_template("stores.html", stores=store_data)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect(url_for('main.home'))

    