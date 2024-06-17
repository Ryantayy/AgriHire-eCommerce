
import re
from agrihire.dbconnection import getCursor
from agrihire import my_hashing
from flask import session, flash
from datetime import datetime, timedelta
from decimal import Decimal
import base64
import logging


def format_date(input_date):
    formatted_date = datetime.strptime(
        str(input_date), '%Y-%m-%d').strftime('%d/%m/%Y')
    return formatted_date


def format_time(input_time):
    formatted_time = datetime.strptime(
        str(input_time), '%H:%M:%S').strftime('%H:%M')
    return formatted_time


def format_datetime(input_datetime):
    formatted_datetime = datetime.strptime(
        str(input_datetime), '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M')
    return formatted_datetime

def parse_datetime(date_string):
    return datetime.strptime(date_string, '%d/%m/%Y %H:%M')

def format_currency(value):
    return f"${value:,.2f}"

def parse_currency(value):
    """Convert formatted currency string to Decimal for calculations."""
    # Remove any currency symbols and commas
    number_string = re.sub(r'[^\d.]', '', value)
    return Decimal(number_string)

def hash_password(password):
    hashed_password = my_hashing.hash_value(password, salt='myhashsalt')
    return hashed_password

def user_exists_with_email(email):
    if get_user_by_email(email):
        return True
    else:
        return False

def get_user_by_email(email):
    conn = getCursor()
    # Get the user info from db
    conn.execute('SELECT * FROM User WHERE email = %s', (email,))
    user = conn.fetchone()
    return user

def get_customer_by_user_id(user_id):
    conn = getCursor()
    # Get the user info from db
    conn.execute("""SELECT u.*, c.* FROM User u
                LEFT JOIN Customer c ON u.user_id = c.user_id WHERE u.user_id = %s""", (user_id,))
    user = conn.fetchone()
    return user

def get_user_full_name():
    email = session['email']
    user = get_user_by_email(email)
    name = f"{user['first_name']} {user['last_name']}"
    return name

def get_user_titles():
    conn = getCursor()
    conn.execute('SELECT DISTINCT title FROM Customer')
    titles = conn.fetchall()
    titles_list = [title['title'] for title in titles]  # Extract titles from tuples
    return titles_list


def register_new_customer(title, firstname, lastname, email, phone, hashed_password, date_of_birth, address):
    conn = getCursor()
    # Insert the new user to db
    conn.execute("INSERT INTO User (email, password, role_id) VALUES (%s, %s, %s)", (email, hashed_password, 1))
    # Get the user id
    user_id = conn.lastrowid
    # Insert the new customer to db
    conn.execute("INSERT INTO Customer (user_id, title, first_name, last_name, phone, address, date_of_birth) VALUES (%s, %s, %s, %s, %s, %s, %s)", (user_id, title, firstname, lastname, phone, address, date_of_birth))
    conn.close()
    
def reset_password(email, hashed_password):
    conn = getCursor()
    conn.execute("UPDATE User SET password = %s WHERE email = %s", (hashed_password, email))
    conn.close()

def get_all_equipment_overall_details(category_id):
    conn = getCursor()
    conn.execute(""" 
        SELECT DISTINCT 
        c.category_name AS category_name, 
        e.name AS name, 
        sub.hire_cost AS original_hire_cost,
        IF(p.discount_rate IS NOT NULL AND CURDATE() BETWEEN p.start_date AND p.end_date,
        sub.hire_cost * (1 - p.discount_rate / 100),
        sub.hire_cost) AS hire_cost,
        e.equipment_id,
        e.sub_category_id,
        e.purchase_date,
        s.store_id, 
        (SELECT MIN(image_url) 
        FROM Images 
        WHERE sub_category_id = e.sub_category_id) AS image_url,
        p.discount_rate,
        p.start_date,
        p.end_date
    FROM 
        Equipment e
    INNER JOIN 
        Category c ON e.category_id = c.category_id
    INNER JOIN 
        Sub_Category sub ON e.sub_category_id = sub.sub_category_id
    LEFT JOIN 
        Store s ON e.store_id = s.store_id
    LEFT JOIN 
        Promotions p ON sub.sub_category_id = p.sub_category_id AND CURDATE() BETWEEN p.start_date AND p.end_date
    WHERE 
          c.category_id = %s; """,(category_id,))
    equipments = conn.fetchall()
    seen_sub_categories = set()
    unique_equipments = []
    
    for equipment in equipments:
        sub_category_id = equipment['sub_category_id']
        if sub_category_id not in seen_sub_categories:
            equipment['hire_cost'] = "{:.2f}".format(float(equipment['hire_cost']))
            equipment['original_hire_cost'] = "{:.2f}".format(float(equipment['original_hire_cost']))
            unique_equipments.append(equipment)
            seen_sub_categories.add(sub_category_id)
    
    return unique_equipments

def count_num_of_product():
    conn = getCursor()
    conn.execute("""SELECT COUNT(equipment_id) AS count
        FROM Equipment;""")
    number_of_equipments = conn.fetchone()
    return number_of_equipments

def count_num_of_product_with_category(category_id):
    conn = getCursor()
    conn.execute("""SELECT COUNT(equipment_id)
        FROM Equipment
        WHERE category_id = %s;""", (category_id,))
    number_of_equipments = conn.fetchone()
    return number_of_equipments

def count_num_of_product_with_category_and_store(category_id, store_id):
    conn = getCursor()
    conn.execute(""""SELECT COUNT(equipment_id)
        FROM Equipment
        WHERE category_id = %s AND store_id = %s;""",(category_id, store_id,))
    number_of_equipments = conn.fetchone()
    return number_of_equipments

def get_category_name_by_category_id(category_id):
    conn = getCursor()
    conn.execute("""SELECT category_name
        FROM Category
        WHERE category_id = %s;""", (category_id,))
    category_name = conn.fetchone()
    return category_name

def get_equipment_details_by_sub_category_id(sub_category_id):
    conn = getCursor()
    
    today = datetime.now().date()
    # Updated SQL query to also fetch any active promotion rates
    conn.execute("""
            SELECT 
            c.category_id,
            c.category_name AS category_name,
            e.name AS name,
            e.sub_category_id,
            e.serial_number AS serial_number,
            s.store_name AS store_name,
            sub.hire_cost AS original_hire_cost,
            e.equipment_id,
            sub.description,
            sub.weight,
            sub.dimension,
            sub.shipping_price,
            sub.min_hire_period,
            sub.max_hire_period,
            e.equipment_condition,
            e.equipment_status,
            es.available_quantity,
            i.image_id,
            i.image_url,
            p.discount_rate
            FROM Equipment e 
            INNER JOIN Category c ON e.category_id = c.category_id
            INNER JOIN Sub_Category sub ON e.sub_category_id = sub.sub_category_id
            INNER JOIN Store s ON e.store_id = s.store_id
            INNER JOIN Equipment_Stock es ON e.sub_category_id = es.sub_category_id AND es.available_quantity > 0
            INNER JOIN Images i ON sub.sub_category_id = i.sub_category_id
            LEFT JOIN Promotions p ON e.sub_category_id = p.sub_category_id AND %s BETWEEN p.start_date AND p.end_date
            WHERE e.sub_category_id = %s AND e.equipment_status = 'available'
            ORDER BY e.equipment_id
            LIMIT 1;
        """, (today, sub_category_id))

    equipment = conn.fetchone()
    conn.close()

    if equipment:

        # If there's a promotion and it's active, adjust the hire cost
        if equipment['discount_rate']:
            discount_rate = Decimal(equipment['discount_rate'])
            discounted_hire_cost = Decimal(equipment['original_hire_cost']) * (1 - discount_rate / 100)
            equipment['hire_cost'] = discounted_hire_cost
        else:
            # No active promotion, hire_cost is the original
            equipment['hire_cost'] = Decimal(equipment['original_hire_cost'])
        
        # Include the original hire cost for clarity
        equipment['original_rate'] = Decimal(equipment['original_hire_cost'])
        equipment['original_rate']

    return equipment

def get_available_equipment(sub_category_id, store_id, start_datetime, end_datetime, user_id):
    conn = getCursor()
    conn.execute("""
                SELECT 
            c.category_id, c.category_name AS category_name, e.name AS name, e.serial_number AS serial_number,
            s.store_name AS store_name, sub.hire_cost AS original_hire_cost, e.equipment_id, sub.description, 
            sub.weight, sub.dimension, sub.shipping_price, sub.min_hire_period, sub.max_hire_period, e.equipment_condition,
            i.image_id, i.image_url, p.discount_rate, es.available_quantity
        FROM Equipment e 
        INNER JOIN Category c ON e.category_id = c.category_id
        INNER JOIN Sub_Category sub ON e.sub_category_id = sub.sub_category_id
        INNER JOIN Store s ON e.store_id = s.store_id
        INNER JOIN Equipment_Stock es ON e.sub_category_id = es.sub_category_id
        INNER JOIN Images i ON sub.image_id = i.image_id
        LEFT JOIN Promotions p ON e.sub_category_id = p.sub_category_id 
                                  AND CURDATE() BETWEEN p.start_date AND p.end_date
        WHERE e.sub_category_id = %s AND e.store_id = %s
          AND e.equipment_status = 'available'
          AND NOT EXISTS (
              SELECT 1 FROM Bookings b
              WHERE b.equipment_id = e.equipment_id
                AND b.status NOT IN ('cancelled', 'returned')
                AND ((b.checkout_datetime < %s AND b.return_datetime > %s)
                     OR (b.checkout_datetime < %s AND b.return_datetime > %s))
          )
          AND NOT EXISTS (
              SELECT 1 FROM Cart c
              WHERE c.user_id = %s AND c.equipment_id = e.equipment_id
                AND ((c.checkout_datetime < %s AND c.return_datetime > %s)
                     OR (c.checkout_datetime < %s AND c.return_datetime > %s))
          )
        ORDER BY (SELECT COUNT(*) FROM Cart c WHERE c.equipment_id = e.equipment_id AND c.user_id = %s) ASC, e.equipment_id
        LIMIT 1;
    """, (sub_category_id, store_id, end_datetime, start_datetime, start_datetime, end_datetime, 
          user_id, end_datetime, start_datetime, start_datetime, end_datetime, user_id))
    equipment = conn.fetchone()
    conn.close()

    if equipment:
        # If there's a promotion and it's active, adjust the hire cost
        if equipment.get('discount_rate'):
            discount_rate = Decimal(equipment['discount_rate'])
            discounted_hire_cost = Decimal(equipment['original_hire_cost']) * (1 - discount_rate / 100)
            equipment['hire_cost'] = discounted_hire_cost
        else:
            equipment['hire_cost'] = Decimal(equipment['original_hire_cost'])

        return equipment
    else:
        return None

def is_equipment_in_cart(user_id, equipment_id, start_datetime, end_datetime):
    conn = getCursor()
    try:
        conn.execute("""
            SELECT COUNT(*) AS count
            FROM Cart c
            JOIN Equipment e ON c.equipment_id = e.equipment_id
            WHERE c.user_id = %s
                AND e.equipment_id = %s
                AND ((c.checkout_datetime <= %s AND c.return_datetime >= %s)
                     OR (c.checkout_datetime <= %s AND c.return_datetime >= %s))
        """, (user_id, equipment_id, end_datetime, start_datetime, start_datetime, end_datetime))
        result = conn.fetchone()
        if result is None:
            return False  # No rows were found, indicating the equipment is not in the cart
        return result['count'] > 0  # Check if the count is greater than zero and return True/False
    finally:
        conn.close()


def get_all_category():
    conn = getCursor()
    conn.execute("""SELECT category_id, category_name, REPLACE( category_name, ' ', '') AS category_no_space FROM Category ORDER BY category_id asc;""")
    category_list = conn.fetchall()

    return category_list

def get_sub_category_by_category(category_id):
    conn = getCursor()
    conn.execute("""SELECT sub_category_id, sub_category_name, REPLACE( sub_category_name, ' ', '') AS sub_category_no_space FROM Sub_Category WHERE category_id = %s ORDER BY sub_category_id asc;""",(category_id,))
    sub_category_list = conn.fetchall()

    return sub_category_list


def get_equipments_by_category_id(category_id):
    conn = getCursor()
    conn.execute("""SELECT e.sub_category_id, 
                           MIN(e.equipment_id) AS equipment_id, 
                           e.category_id, e.sub_category_id,
                           c.category_name, 
                           MIN(e.name) AS name 
                    FROM Equipment e 
                    LEFT JOIN Category c ON e.category_id = c.category_id
                    WHERE e.category_id = %s 
                    GROUP BY e.sub_category_id, e.category_id, c.category_name;""", (category_id,))
    equipments_with_category = conn.fetchall()

    return equipments_with_category

def get_all_stores():
    conn = getCursor()
    conn.execute("""SELECT s.store_id, s.store_name, s.address, i.image_url 
                 FROM Store s
                 JOIN Images i ON s.image_id = i.image_id
                 ORDER BY store_id ASC;""")
    store_list = conn.fetchall()
    return store_list



def get_equipments_for_stores(store_name, category_id):
    conn = getCursor()
    conn.execute("""SELECT store_id FROM Store WHERE store_name in (%s)""", store_name)
    store_ids  = conn.fetchall()
    conn.execute("""SELECT e.equipment_id, e.category_id, c.category_name, e.name FROM Equipment e
                    LEFT JOIN Category c on e.category_id = c.category_id
                    WHERE e.store_id in %s AND e.category_id = %s;""",(store_ids,category_id))
    equipments_with_category = conn.fetchall()

    return equipments_with_category
    
def update_customer_profile(title, firstname, lastname, email, phone, address, date_of_birth):
    conn = getCursor()
    conn.execute("UPDATE User SET email = %s WHERE user_id = %s", (email, session['user_id']))
    
    # Update the customer details in the customer table
    conn.execute("UPDATE Customer SET title = %s, first_name = %s, last_name = %s, phone = %s, address = %s, date_of_birth = %s WHERE user_id = %s",
                 (title, firstname, lastname, phone, address, date_of_birth, session['user_id']))
    conn.close()

def get_customer_bookings(user_id):
    conn = getCursor()
    conn.execute("""SELECT b.*, e.*, p.*, i.*, o.*
                    FROM Bookings b
                    LEFT JOIN Equipment e ON b.equipment_id = e.equipment_id
                    LEFT JOIN User u ON b.user_id = u.user_id
                    LEFT JOIN Sub_Category sub ON e.sub_category_id = sub.sub_category_id
                    LEFT JOIN Images i ON sub.sub_category_id = i.sub_category_id
                    LEFT JOIN OrderBookings ob ON b.booking_id = ob.booking_id
                    LEFT JOIN Orders o ON ob.order_id = o.order_id
                    LEFT JOIN Payments p ON o.payment_id = p.payment_id
                    WHERE u.user_id = %s""", (user_id,))
                    
                    
    bookings = conn.fetchall()

    for booking in bookings:
        # Convert to NZ time format
        booking['checkout_datetime'] = format_datetime(booking['checkout_datetime'])
        booking['return_datetime'] = format_datetime(booking['return_datetime'])
    return bookings

def get_customer_orders(customer_id):
    conn = getCursor()
    conn.execute("""SELECT DISTINCT p.*, o.*
                    FROM Orders o
                    LEFT JOIN OrderBookings ob ON o.order_id = ob.order_id
                    LEFT JOIN Bookings b ON ob.booking_id = b.booking_id
                    LEFT JOIN Customer c ON c.customer_id = o.customer_id
                    LEFT JOIN Payments p ON o.payment_id = p.payment_id
                    WHERE o.status != 'cancelled' AND o.customer_id = %s
                    ORDER BY o.order_date DESC
                    ;""", (customer_id,))
                    
    orders = conn.fetchall()

    for order in orders:
        # Convert to NZ time format
        order['order_date'] = format_datetime(order['order_date'])
    return orders

def get_all_orders():
    conn = getCursor()
    conn.execute("""SELECT o.order_id, o.order_date, p.amount, c.user_id, CONCAT(c.first_name, ' ', c.last_name) AS customer_name
                    FROM Orders o
                    INNER JOIN Customer c ON o.customer_id = c.customer_id
                    INNER JOIN Payments p ON o.payment_id = p.payment_id
                    ORDER BY o.order_date DESC;""")
    orders = conn.fetchall()
    for order in orders:
        # Convert to NZ time format
        order['order_date'] = format_datetime(order['order_date'])
    return orders

def get_all_orders_by_store(store_id):
    conn = getCursor()
    conn.execute("""SELECT 
                    o.order_id, 
                    MAX(p.payment_id) AS payment_id, 
                    MAX(p.amount) AS payment_amount, 
                    MAX(p.payment_date) AS payment_date, 
                    MAX(u.user_id) AS user_id, 
                    MAX(c.address) AS address, 
                    MAX(c.phone) AS phone, 
                    MAX(u.email) AS email, 
                    MAX(o.order_date) AS order_date, 
                    MAX(o.payment_method) AS payment_method, 
                    MAX(o.special_instruction) AS special_instruction, 
                    MAX(o.status) AS status,
                    SUM(b.line_total) AS amount,
                    CONCAT(c.first_name, ' ', c.last_name) AS customer_name
                FROM 
                    Orders o
                    INNER JOIN Payments p ON p.payment_id = o.payment_id
                    INNER JOIN Customer c ON c.customer_id = o.customer_id
                    INNER JOIN User u ON c.user_id = u.user_id
                    INNER JOIN OrderBookings ob ON o.order_id = ob.order_id
                    INNER JOIN Bookings b ON ob.booking_id = b.booking_id
                    INNER JOIN Equipment e ON b.equipment_id = e.equipment_id     
                WHERE 
                    e.store_id = %s
                GROUP BY 
                    o.order_id;""",(store_id,))
    orders = conn.fetchall()
    for order in orders:
        # Convert to NZ time format
        order['order_date'] = format_datetime(order['order_date'])
    return orders

def get_order_by_order_id(order_id):
    conn = getCursor()
    conn.execute("""SELECT o.order_id, p.payment_id, p.amount, p.payment_date, u.user_id, CONCAT(c.first_name, ' ', c.last_name) As customer_name, o.shipping_address as address, c.phone, u.email , o.order_date, o.payment_method, o.special_instruction, o.status
                    FROM Orders o
                    INNER JOIN Payments p ON p.payment_id = o.payment_id
                    INNER JOIN Customer c ON c.customer_id = o.customer_id
                    INNER JOIN User u ON c.user_id = u.user_id
                    WHERE order_id = %s;""",(order_id,))
    order = conn.fetchone()
    order['payment_date'] = format_datetime(order['payment_date'])
    order['order_date'] = format_datetime(order['order_date'])
    return order


def get_orders_info_for_this_week(store_id):
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)
    
    start_of_week_str = start_of_week.strftime('%Y-%m-%d %H:%M:%S')
    end_of_week_str = end_of_week.strftime('%Y-%m-%d %H:%M:%S')

    conn = getCursor()
    conn.execute("""SELECT DISTINCT(o.order_id), p.amount, o.order_date, c.user_id, CONCAT(c.first_name, ' ', c.last_name) As customer_name, o.status
                    FROM Orders o
					INNER JOIN OrderBookings ob ON ob.order_id = o.order_id
					INNER JOIN Bookings b ON ob.booking_id = b.booking_id
                    INNER JOIN Customer c ON o.customer_id = c.customer_id
                    INNER JOIN Payments p ON o.payment_id = p.payment_id
                    INNER JOIN Equipment e ON b.equipment_id = e.equipment_id
                    WHERE e.store_id = %s AND o.order_date BETWEEN %s AND %s
                """, (store_id, start_of_week_str, end_of_week_str,))
    orders = conn.fetchall()
    for order in orders:
        # Convert to NZ time format
        order['order_date'] = format_datetime(order['order_date'])
    return orders

def get_orders_info_for_today_pickup(store_id):
    conn = getCursor()
    query = """
        SELECT DISTINCT(o.order_id), p.amount, o.order_date, c.user_id, CONCAT(c.first_name, ' ', c.last_name) AS customer_name, o.status
        FROM Orders o
        INNER JOIN OrderBookings ob ON ob.order_id = o.order_id
        INNER JOIN Bookings b ON ob.booking_id = b.booking_id
        INNER JOIN Customer c ON o.customer_id = c.customer_id
        INNER JOIN Payments p ON o.payment_id = p.payment_id
        INNER JOIN Equipment e ON b.equipment_id = e.equipment_id
        WHERE e.store_id = %s AND o.shipping_address = 'Self-Pickup' ;
    """
    conn.execute(query, (store_id,))
    pre_orders = conn.fetchall()
    today = datetime.today().date()
    orders = [
        order for order in pre_orders
        if order['order_date'].date() == today
    ]
   
    for order in orders:
        # Convert to NZ time format
        order['order_date'] = format_datetime(order['order_date'])
    return orders

def get_orders_info_for_today_shipping(store_id):
    conn = getCursor()
    query = """
        SELECT DISTINCT(o.order_id), p.amount, o.order_date, c.user_id, CONCAT(c.first_name, ' ', c.last_name) AS customer_name, o.status
        FROM Orders o
        INNER JOIN OrderBookings ob ON ob.order_id = o.order_id
        INNER JOIN Bookings b ON ob.booking_id = b.booking_id
        INNER JOIN Customer c ON o.customer_id = c.customer_id
        INNER JOIN Payments p ON o.payment_id = p.payment_id
        INNER JOIN Equipment e ON b.equipment_id = e.equipment_id
        WHERE e.store_id = %s AND o.shipping_address != 'Self-Pickup' ;
    """
    conn.execute(query, (store_id,))
    pre_orders = conn.fetchall()
    today = datetime.today().date()
    orders = [
        order for order in pre_orders
        if order['order_date'].date() == today
    ]
   
    for order in orders:
        # Convert to NZ time format
        order['order_date'] = format_datetime(order['order_date'])
    return orders

def get_booking_info_by_order_id(order_id):
    conn = getCursor()
    conn.execute("""SELECT b.checkout_datetime, b.return_datetime, b.line_total, u.email, cu.phone, cu.address, s.shipping_price, b.status, e.name, s.description, e.serial_number, st.store_name, 
                    c.category_name, s.sub_category_name, u.email, p.amount, p.payment_date, CONCAT(cu.first_name, ' ', cu.last_name) As customer_name, p.payment_id, u.user_id, 
                    e.equipment_id, st.store_id, b.booking_id, o.payment_method, i.image_url
                    FROM Orders o
                    INNER JOIN OrderBookings ob ON ob.order_id = o.order_id
                    LEFT JOIN Bookings b ON ob.booking_id = b.booking_id
                    LEFT JOIN Equipment e ON b.equipment_id = e.equipment_id
                    LEFT JOIN Category c ON c.category_id = e.category_id
                    LEFT JOIN Sub_Category s ON s.sub_category_id = e.sub_category_id
                    LEFT JOIN Store st ON st.store_id = e.store_id
                    LEFT JOIN User u ON b.user_id = u.user_id
                    LEFT JOIN Customer cu ON cu.user_id = u.user_id
                    LEFT JOIN Images i ON e.sub_category_id = i.sub_category_id
                    LEFT JOIN Payments p ON o.payment_id = p.payment_id
                    WHERE o.order_id = %s;
                """, (order_id,))
    bookings = conn.fetchall()
    for booking in bookings:
        # Convert to NZ time format
        booking['checkout_datetime'] = format_datetime(booking['checkout_datetime'])
        booking['return_datetime'] = format_datetime(booking['return_datetime'])
        booking['payment_date'] = format_datetime(booking['payment_date'])
    return bookings

#for unit testing clean up the testing data
def delete_user_for_unit_testing(email):
    conn = getCursor()
    conn.execute("SELECT * FROM User WHERE email = %s", (email,))
    user_data = conn.fetchone()
    if user_data:
        user_id = user_data['user_id']
        conn.execute("DELETE FROM Customer WHERE user_id = %s", (user_id,))
        conn.execute("DELETE FROM User WHERE email = %s", (email,))
        conn.close()

def get_customer_payment_methods(user_id):
    conn = getCursor()
    conn.execute("SELECT * FROM PaymentMethods WHERE user_id = %s", (user_id,))
    bank_card_details = conn.fetchall()
    return bank_card_details

def customer_add_payment_method(user_id, card_type, name_on_card, expiration_month, expiration_year, digits, security_code):
    conn = getCursor()
    conn.execute("INSERT INTO PaymentMethods (user_id, card_type, name_on_card, expiration_month, expiration_year, digits, security_code) VALUES (%s, %s, %s, %s, %s, %s, %s)", (user_id, card_type, name_on_card, expiration_month, expiration_year, digits, security_code))
    conn.close()

def get_store_list():
    conn = getCursor()
    conn.execute("""SELECT DISTINCT store_id, store_name FROM  Store;""")
    stores = conn.fetchall()
    store_list = [{'store_id': store['store_id'], 'store_name': store['store_name']} for store in stores]
    return store_list

def is_equipment_available(equipment_id, start_datetime, end_datetime):
    conn = getCursor()

    start_datetime_str = start_datetime.strftime('%Y-%m-%d %H:%M:%S')
    end_datetime_str = end_datetime.strftime('%Y-%m-%d %H:%M:%S')

    query = """
        SELECT COUNT(*) as count
        FROM Bookings b
        JOIN Equipment e ON b.equipment_id = e.equipment_id
        WHERE b.equipment_id = %s AND (
            (b.checkout_datetime < %s AND b.return_datetime > %s)
        )
    """

    conn.execute(query, (equipment_id, end_datetime_str, start_datetime_str))
    count = conn.fetchone()['count']
    return count == 0

def is_store_available_for_equipment(store_id, equipment_id):
    conn = getCursor()
    query = """
        SELECT COUNT(*) as count FROM Equipment
        WHERE store_id = %s AND equipment_id = %s 
    """
    conn.execute(query, (store_id, equipment_id))
    result = conn.fetchone()
    return result['count'] > 0

def get_hire_cost(sub_category_id):
    conn = getCursor()
    # Get the base hire cost from the Equipment table
    conn.execute("SELECT DISTINCT hire_cost FROM Sub_Category WHERE sub_category_id = %s", (sub_category_id,))
    hire_cost = conn.fetchone()['hire_cost']

    # Check if there is an active promotion for this equipment
    today = datetime.now().date()
    conn.execute("SELECT discount_rate FROM Promotions WHERE sub_category_id = %s AND %s BETWEEN start_date AND end_date",
                 (sub_category_id, today))
    promotion = conn.fetchone()

    if promotion:
        discount_rate = promotion['discount_rate']
        # Apply the discount rate to calculate the final hire cost
        hire_cost *= (1 - (discount_rate / 100))

    conn.close()
    return hire_cost

def get_display_rates(sub_category_id):
    conn = getCursor()
    # Get the base hire cost from the Equipment table
    conn.execute("SELECT DISTINCT hire_cost FROM Sub_Category WHERE sub_category_id = %s", (sub_category_id,))
    hire_rate_row = conn.fetchone()
    
    if hire_rate_row is None:
        conn.close()
        return "N/A", "N/A", "N/A"  # Return 'N/A' if the equipment is not found

    hire_rate = Decimal(hire_rate_row['hire_cost'])
    discounted_rate = "N/A"  # Default no discount
    discount_rate = "N/A"  # Default no discount

    # Check for an active promotion
    today = datetime.now().date()
    conn.execute("SELECT discount_rate FROM Promotions WHERE sub_category_id = %s AND %s BETWEEN start_date AND end_date",
                 (sub_category_id, today))
    promotion = conn.fetchone()

    # Calculate discounted rate if there is an active promotion
    if promotion:
        discount_rate = Decimal(promotion['discount_rate'])
        discounted_rate = hire_rate * (1 - (discount_rate / 100))
        discounted_rate = format_currency(discounted_rate)
        discount_rate = f"{discount_rate}%"  # Display as a percentage

    hire_rate = format_currency(hire_rate)  # Format for display

    conn.close()
    return hire_rate, discounted_rate, discount_rate


def add_hire_booking_to_cart(user_id, equipment_id, start_datetime, end_datetime, total_cost):
    conn = getCursor()
    conn.execute("SELECT quantity FROM Cart WHERE user_id = %s AND equipment_id = %s AND checkout_datetime = %s AND return_datetime = %s",
                    (user_id, equipment_id, start_datetime, end_datetime))
    result = conn.fetchone()

    if result:
        conn.execute("UPDATE Cart SET quantity = quantity + 1, total_cost = total_cost + %s WHERE user_id = %s AND equipment_id = %s AND checkout_datetime = %s AND return_datetime = %s",
                        (total_cost, user_id, equipment_id, start_datetime, end_datetime))
    else:
        conn.execute("INSERT INTO Cart (user_id, equipment_id, checkout_datetime, return_datetime, quantity, total_cost) VALUES (%s, %s, %s, %s, %s, %s)",
                        (user_id, equipment_id, start_datetime, end_datetime, 1, total_cost))


def get_hire_periods(sub_category_id):
    conn = getCursor()
    query = """
        SELECT min_hire_period, max_hire_period
        FROM Sub_Category
        WHERE sub_category_id = %s
    """
    conn.execute(query, (sub_category_id,))
    result = conn.fetchone()
    return result['min_hire_period'], result['max_hire_period']

def get_staff_by_user_id(user_id):
    conn = getCursor()
  
    conn.execute("""SELECT u.*, s.* FROM User u
                LEFT JOIN Staff s ON u.user_id = s.user_id WHERE u.user_id = %s""", (user_id,))
    user = conn.fetchone()
    return user

def update_staff_profile(title, firstname, lastname, email, phone, address):
    conn = getCursor()
    conn.execute("UPDATE User SET email = %s WHERE user_id = %s", (email, session['user_id']))
    
    # Update the staff details in the staff table
    conn.execute("UPDATE Staff SET title = %s, first_name = %s, last_name = %s, phone = %s, address = %s WHERE user_id = %s",
                 (title, firstname, lastname, phone, address, session['user_id']))
    conn.close()

def get_shop_cart_items(user_id):
    conn = getCursor()
    conn.execute("""SELECT c.*, e.*, i.*, sub.*, s.store_name
                    FROM Cart c
                    INNER JOIN Equipment e ON c.equipment_id = e.equipment_id
                    LEFT JOIN Sub_Category sub ON e.sub_category_id = sub.sub_category_id
                    LEFT JOIN Store s ON e.store_id = s.store_id
                    INNER JOIN Images i ON sub.image_id = i.image_id
                    WHERE c.user_id = %s""", (user_id,))
    cart_items = conn.fetchall()

    for item in cart_items:
        item['total_cost'] = format_currency(Decimal(item['total_cost']))
        item['checkout_datetime'] = format_datetime(item['checkout_datetime'])
        item['return_datetime'] = format_datetime(item['return_datetime'])

    return cart_items

def calculate_subtotals(cart_items):
    gst_rate = Decimal('0.15')  # Assuming a GST rate of 15%
    # Calculate item subtotal as GST-exclusive
    item_subtotal_excl_gst = sum(Decimal(item['total_cost'].replace('$', '').replace(',', '')) / (1 + gst_rate) for item in cart_items)
    gst = item_subtotal_excl_gst * gst_rate
    subtotal = item_subtotal_excl_gst + gst

    # Calculate the total shipping cost
    shipping_total = sum(item['shipping_price'] for item in cart_items if item['shipping_price'])

    # Format all values as currency
    formatted_item_subtotal_excl_gst = format_currency(item_subtotal_excl_gst)
    formatted_gst = format_currency(gst)
    formatted_subtotal = format_currency(subtotal)

    return formatted_item_subtotal_excl_gst, formatted_gst, formatted_subtotal, shipping_total

def delete_cart_item(cart_id):
    conn = getCursor()
    conn.execute("DELETE FROM Cart WHERE cart_id = %s", (cart_id,))
    conn.close()
    
def add_products(name, serial_number, category_id, sub_category_id, store_id,purchase_date,purchase_cost,equipment_condition,equipment_status):
    conn = getCursor()
    conn.execute("INSERT INTO Equipment (name, serial_number, category_id, sub_category_id, store_id,purchase_date,purchase_cost,equipment_condition,equipment_status) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (name, serial_number, category_id, sub_category_id, store_id,purchase_date,purchase_cost,equipment_condition,equipment_status))
    conn.close()

# manager type = 0 means local manager, mamager_type = 1 means national manager
def get_manager_by_user_id(user_id, manager_type):
    conn = getCursor()
    if manager_type == 0:
        conn.execute("""SELECT u.*, l.* FROM User u
                    LEFT JOIN Local_Manager l ON u.user_id = l.user_id WHERE u.user_id = %s""", (user_id,))
    elif manager_type == 1:
        conn.execute("""SELECT u.*, n.* FROM User u
                    LEFT JOIN National_Manager n ON u.user_id = n.user_id WHERE u.user_id = %s""", (user_id,))
    user = conn.fetchone()
    return user

def update_manager_profile(title, firstname, lastname, email, phone, address, manager_type):
    conn = getCursor()
    conn.execute("UPDATE User SET email = %s WHERE user_id = %s", (email, session['user_id']))
    
    if manager_type == 0:
        # Update the staff details in the local manager table
        conn.execute("UPDATE Local_Manager SET title = %s, first_name = %s, last_name = %s, phone = %s, address = %s WHERE user_id = %s",
                    (title, firstname, lastname, phone, address, session['user_id']))
    elif manager_type == 1:
        # Update the staff details in the local manager table
        conn.execute("UPDATE National_Manager SET title = %s, first_name = %s, last_name = %s, phone = %s, address = %s WHERE user_id = %s",
                    (title, firstname, lastname, phone, address, session['user_id']))

    conn.close()

def get_store_id_by_user_id(user_id):
    conn = getCursor()
    conn.execute("""SELECT store_id
                    FROM Local_Manager l 
                    WHERE user_id = %s ;""",(user_id,))
    store_id = conn.fetchone()
    return store_id

def get_store_id_by_staff_user_id(user_id):
    conn = getCursor()
    conn.execute("""SELECT store_id
                    FROM Staff l 
                    WHERE user_id = %s ;""",(user_id,))
    store_id = conn.fetchone()
    return store_id

def get_all_staffs():
    conn = getCursor()
    conn.execute("""SELECT u.email, s.user_id, s.address, s.phone, concat(s.first_name , ' ' , s.last_name) AS staff_name,
                    CASE WHEN s.status = 0 THEN 'Inactive' ELSE 'Active' END AS status, st.store_name 
                    FROM Staff s 
                    INNER JOIN User u ON s.user_id = u.user_id
                    INNER JOIN Store st ON st.store_id = s.store_id;""")
    staffs = conn.fetchall()
    return staffs

def get_all_staffs_by_store_id(store_id):
    conn = getCursor()
    conn.execute("""SELECT u.email, s.user_id, s.address, s.phone, concat(s.first_name , ' ' , s.last_name) AS staff_name,
                    CASE WHEN s.status = 0 THEN 'Inactive' ELSE 'Active' END AS status, st.store_name 
                    FROM Staff s 
                    INNER JOIN User u ON s.user_id = u.user_id
                    INNER JOIN Store st ON st.store_id = s.store_id
                    WHERE st.store_id = %s;""",(store_id,))
    staffs = conn.fetchall()
    return staffs

def deactive_staff_by_user_id(user_id):
    conn = getCursor()
    conn.execute("""UPDATE Staff SET status = 0 WHERE user_id = %s;""",(user_id,))

def get_all_stores_list():
    conn = getCursor()
    conn.execute('SELECT store_name FROM Store')
    stores = conn.fetchall()
    stores_list = [store["store_name"] for store in stores]
    return stores_list

def get_store_name_by_id(store_id):
    conn = getCursor()
    conn.execute('SELECT store_name FROM Store WHERE store_id = %s',(store_id,))
    store = conn.fetchone()
    return store 

def get_store_id_by_store_name(store_name):
    conn = getCursor()
    conn.execute('SELECT store_id FROM Store WHERE store_name = %s',(store_name,))
    store = conn.fetchone()
    return store 

def get_stores_with_available_equipment(sub_category_id):
    # Assuming you have a function to connect to the database
    conn = getCursor()  # Your function to connect to the database
    conn.execute( """
        SELECT DISTINCT s.store_id, s.store_name
        FROM Store s
        JOIN Equipment_Stock es ON s.store_id = es.store_id
        WHERE es.sub_category_id = %s
    """, (sub_category_id,))
    stores = conn.fetchall()

    return stores

def add_staff(title_id, email, firstname, lastname, phone, address, store, password):
    hashed_password = hash_password(password)
    store_id = get_store_id_by_store_name(store)
    conn = getCursor()
 
    # Insert the new user to db
    conn.execute("INSERT INTO User (email, password, role_id) VALUES (%s, %s, %s)", (email, hashed_password, 2))
    # Get the user id
    user_id = conn.lastrowid
    # Insert the new staff to db
    conn.execute("INSERT INTO Staff (user_id, title, first_name, last_name, phone, address, store_id, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (user_id, title_id, firstname, lastname, phone, address, store_id["store_id"], 1))
    conn.close

def get_staff_details_by_user_id(user_id):
    conn = getCursor()
    conn.execute("""SELECT u.*, s.* , st.store_id, st.store_name FROM User u
                    LEFT JOIN Staff s ON u.user_id = s.user_id 
                    LEFT JOIN Store st ON s.store_id = st.store_id
                    WHERE u.user_id = %s""", (user_id,))
 
    user = conn.fetchone()
    return user

def update_staff(user_id, title_id, email, firstname, lastname, phone, address, store):
    store_id = get_store_id_by_store_name(store)
    conn = getCursor()
    conn.execute("UPDATE User SET email = %s WHERE user_id = %s", (email, user_id))

    conn.execute("UPDATE Staff SET title = %s, first_name = %s, last_name = %s, phone = %s, address = %s, store_id = %s WHERE user_id = %s",
                    (title_id, firstname, lastname, phone, address, store_id["store_id"], user_id))
    conn.close

def add_Image(sub_category_id,entity_id,entity_type,image_url):
    conn = getCursor()
    conn.execute("INSERT INTO Images (sub_category_id,entity_id,entity_type,image_url) VALUES (%s,%s,%s,%s)",
                    (sub_category_id,entity_id,entity_type,image_url))
    image_id = conn.lastrowid
    conn.close()

    return image_id

def is_equipment_stock_from_store(sub_category_id,store_id):
    conn = getCursor()
    conn.execute("SELECT * FROM Equipment_Stock WHERE sub_category_id = %s AND store_id = %s;", (sub_category_id,store_id,))
    stock = conn.fetchone()
    return stock

def add_equipment_stock(store_id,sub_category_id,available_quantity):
    conn = getCursor()
    conn.execute("INSERT INTO Equipment_Stock (store_id,sub_category_id,available_quantity) VALUES (%s,%s,%s);", (store_id,sub_category_id,available_quantity,))
    conn.close()
    
def update_equipment_stock(quantity,sub_category_id):
    conn = getCursor()
    conn.execute("UPDATE Equipment_Stock SET available_quantity = available_quantity + %s WHERE sub_category_id = %s;", (quantity,sub_category_id,))
    conn.close()

def process_booking(user_id, equipment_id, checkout_datetime, return_datetime, line_total):
    conn = getCursor()

    conn.execute("INSERT INTO Bookings (user_id, equipment_id, checkout_datetime, return_datetime, status, line_total) VALUES (%s, %s, %s, %s, %s, %s);", 
                 (user_id, equipment_id, checkout_datetime, return_datetime, 'booked', line_total))
    booking_id = conn.lastrowid

    if booking_id:
        conn.execute("DELETE FROM Cart WHERE user_id = %s AND equipment_id = %s;", (user_id, equipment_id))
    conn.close()

    return booking_id

def create_order(shipping_address, special_instructions, customer_id, order_subtotal, user_id):
    conn = getCursor()
    conn.execute("INSERT INTO Payments (amount, user_id, status) VALUES (%s, %s, %s);", 
                 (order_subtotal, user_id, 'processed'))
    payment_id = conn.lastrowid

    conn.execute("""INSERT INTO Orders (shipping_address, special_instruction, payment_method, customer_id, payment_id, status)
    VALUES (%s, %s, %s, %s, %s, %s);""", (shipping_address, special_instructions, 'Credit Card', customer_id, payment_id, 'Confirmed'))
    order_id = conn.lastrowid
    conn.close()
    
    return order_id

def link_order_booking(order_id, booking_id):
    conn = getCursor()
    conn.execute("""INSERT INTO OrderBookings (order_id, booking_id) VALUES (%s, %s)""", (order_id, booking_id))
    conn.close()
    
def check_booking_availability(equipment_id, checkout_datetime, return_datetime):
    conn = getCursor()
    # Query to check for overlapping bookings
    query = """
    SELECT COUNT(*) FROM Bookings
    WHERE equipment_id = %s AND NOT (%s >= return_datetime OR %s <= checkout_datetime)
    """
    conn.execute(query, (equipment_id, checkout_datetime, return_datetime))
    result = conn.fetchone()
    return result['COUNT(*)'] == 0  # Return True if no conflicts, False otherwise

    
def get_all_sub_category_details():
    conn = getCursor()
    conn.execute("SELECT sc.*, c.category_name FROM Sub_Category sc LEFT JOIN Category c ON sc.category_id = c.category_id;")
    subcategories = conn.fetchall()
    return subcategories

def get_sub_category_details_by_id(sub_category_id):
    conn = getCursor()
    conn.execute("SELECT sc.*, c.category_name FROM Sub_Category sc LEFT JOIN Category c ON sc.category_id = c.category_id WHERE sub_category_id = %s;",(sub_category_id,))
    sub_category = conn.fetchone()
    return sub_category

def update_sub_category(hire_cost, shipping_price, min_hire_period, max_hire_period, sub_category_id):
    conn = getCursor()
    conn.execute("""UPDATE Sub_Category SET hire_cost = %s, shipping_price = %s, min_hire_period= %s, max_hire_period= %s
           WHERE sub_category_id = %s;""", (hire_cost, shipping_price, min_hire_period, max_hire_period, sub_category_id,))
    conn.close()

def get_all_equipments():
    conn = getCursor()
    conn.execute("SELECT e.equipment_id, e.serial_number, e.equipment_condition, e.equipment_status, sc.sub_category_name FROM Equipment e LEFT JOIN Sub_Category sc ON e.sub_category_id = sc.sub_category_id ;")
    equipments = conn.fetchall()
    return equipments

def get_all_equipments_by_store_id(store_id):
    conn = getCursor()
    conn.execute("""SELECT e.equipment_id, e.serial_number, e.equipment_condition, sc.sub_category_name, e.equipment_status
    FROM Equipment e 
    LEFT JOIN Sub_Category sc ON e.sub_category_id = sc.sub_category_id 
    WHERE store_id = %s ORDER BY e.equipment_id;""",(store_id,))
    equipments = conn.fetchall()
    return equipments

def get_equipment_details_by_id(id):
    conn = getCursor()
    conn.execute("SELECT e.equipment_id, e.serial_number, e.equipment_condition, sc.sub_category_name, e.equipment_status FROM Equipment e LEFT JOIN Sub_Category sc ON e.sub_category_id = sc.sub_category_id WHERE e.equipment_id = %s;",(id,))
    equipment = conn.fetchone()
    return equipment

def Update_equipment_condition(equipment_id, equipment_condition):
    conn = getCursor()
    conn.execute('SELECT equipment_condition FROM Equipment WHERE equipment_id = %s',(equipment_id,))
    curr_status = conn.fetchone()
    if curr_status['equipment_condition'] == 'out_of_service':
        conn.execute(""" UPDATE Equipment SET equipment_status = %s WHERE equipment_id = %s ;""",('available',equipment_id, ))
    elif equipment_condition == 'out_of_service':
        conn.execute(""" UPDATE Equipment SET equipment_status = %s WHERE equipment_id = %s ;""",('unavailable',equipment_id, ))
    conn.execute(""" UPDATE Equipment SET equipment_condition = %s WHERE equipment_id = %s ;""",(equipment_condition,equipment_id, ))
    conn.close()

def delete_payment_method(card_id):
    conn = getCursor()
    conn.execute("DELETE FROM PaymentMethods WHERE card_id = %s", (card_id,))
    conn.close()

def cancel_order(order_id):
    conn = getCursor()
    try:
        conn.execute("START TRANSACTION;")  # Start a transaction explicitly

        # Check for closeness to booking
        conn.execute("""SELECT b.booking_id FROM Bookings b
                        JOIN OrderBookings ob ON b.booking_id = ob.booking_id
                        WHERE ob.order_id = %s AND TIMESTAMPDIFF(HOUR, NOW(), b.checkout_datetime) < 72;""", (order_id,))
        if conn.fetchone():
            conn.execute("ROLLBACK;")  # Rollback the transaction
            return "Cannot cancel bookings that are within 72 hours and in the past. Please contact staff for cancellation."

        # Cancel the order and related entities
        conn.execute("UPDATE Orders SET status = 'cancelled' WHERE order_id = %s", (order_id,))
        conn.execute("""UPDATE Bookings b
                        JOIN OrderBookings ob ON b.booking_id = ob.booking_id
                        SET b.status = 'cancelled'
                        WHERE ob.order_id = %s;""", (order_id,))
        conn.execute("""UPDATE Payments p
                        JOIN Orders o ON o.payment_id = p.payment_id
                        SET p.status = 'cancelled'
                        WHERE o.order_id = %s;""", (order_id,))

        conn.execute("COMMIT;")  # Commit the transaction
        return None
    except Exception as e:
        conn.execute("ROLLBACK;")  # Ensure rollback on error
        raise Exception(f"Error cancelling order: {e}")  # Consider logging this instead
    finally:
        conn.close()

    
def add_category(category_name):
    conn = getCursor()
    conn.execute("INSERT INTO Category (category_name) VALUES (%s);", (category_name,))
    conn.close()

def count_num_of_sub_category():
    conn = getCursor()
    conn.execute("""SELECT COUNT(sub_category_id) AS count
        FROM Sub_Category;""")
    number_of_sub_category = conn.fetchone()
    return number_of_sub_category

def insert_sub_category(category_id,sub_category_name,hire_cost,image_id,description,weight,dimension,shipping_price):
    conn = getCursor()
    conn.execute("INSERT INTO Sub_Category (category_id,sub_category_name,hire_cost,image_id,description,weight,dimension,shipping_price) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);", (category_id,sub_category_name,hire_cost,image_id,description,weight,dimension,shipping_price,))
    conn.close()

def get_images_by_sub_category_id(sub_category_id):
    conn = getCursor()
    conn.execute("SELECT * FROM Images WHERE sub_category_id = %s;", (sub_category_id,))
    image = conn.fetchone()
    return image

def search_database(query):
    conn = getCursor()
    if not query:  # Check if query is empty or None
        return []  # Return an empty list or handle as appropriate
    
    query = f"%{query}%"
    conn.execute("""
        SELECT 
            filtered_results.sub_category_id,
            filtered_results.name,
            filtered_results.category_id,
            filtered_results.description,
            filtered_results.hire_cost
        FROM (
            SELECT 
                sub.*, 
                e.name AS name,
                ROW_NUMBER() OVER (PARTITION BY sub.sub_category_id ORDER BY e.name) as rn
            FROM Sub_Category sub
            INNER JOIN Equipment e ON sub.sub_category_id = e.sub_category_id
            WHERE e.name LIKE %s
        ) AS filtered_results
        WHERE filtered_results.rn = 1
        """, (query,))

    results = conn.fetchall()
    return results


def add_messsage(user_id, store, subject, message_text):
    store_id = get_store_id_by_store_name(store)
    conn = getCursor()
    conn.execute(""" INSERT INTO Messages (sender_id, store_id, subject, message_text) VALUES (%s,%s,%s,%s)""",(user_id, store_id["store_id"], subject, message_text,))
    conn.close()

def get_message_by_store_id(store_id):
    conn = getCursor()
    conn.execute(""" SELECT m.*, CONCAT(c.first_name, ' ', c.last_name) AS customer_name
    FROM Messages m 
    INNER JOIN Customer c ON m.sender_id = c.user_id 
    WHERE store_id = %s;""",(store_id,))
    messages = conn.fetchall()
    return messages

def cancel_order_and_bookings(order_id):
    conn = getCursor()
    conn.execute("UPDATE Orders SET status = 'cancelled' WHERE Order_id = %s;", (order_id,))
    conn.execute("UPDATE Bookings SET status = 'cancelled' WHERE booking_id in (SELECT booking_id FROM OrderBookings WHERE Order_id = %s);", (order_id,)) 
    conn.execute("UPDATE Payments SET status = 'cancelled' WHERE payment_id = (SELECT payment_id FROM Orders WHERE Order_id = %s);", (order_id,)) 
    conn.close()

def get_all_stores():
    conn = getCursor()
    query = """
    SELECT Store.store_id, Store.store_name, Store.address, Images.image_url
    FROM Store
    LEFT JOIN Images ON Store.image_id = Images.image_id
    ORDER BY Store.store_id ASC;
    """
    conn.execute(query)
    store_list = conn.fetchall()
    return store_list


def get_all_local_managers():
    conn = getCursor()
    try:
        query = """
        SELECT lm.user_id, u.email, u.role_id, lm.first_name, lm.last_name, lm.phone, lm.address, s.store_name, s.address AS store_address
        FROM Local_Manager lm
        JOIN User u ON lm.user_id = u.user_id
        LEFT JOIN Store s ON lm.store_id = s.store_id;
        """
        conn.execute(query)
        managers = conn.fetchall()
        return managers
    finally:
        conn.close()


def add_store_function(store_name, address, image_id):
    conn = getCursor()  
    if image_id:
        conn.execute("INSERT INTO Store (store_name, address, image_id) VALUES (%s, %s, %s)", (store_name, address, image_id))
    else:
        conn.execute("INSERT INTO Store (store_name, address) VALUES (%s, %s)", (store_name, address))
    store_id = conn.lastrowid

    conn.close() 


def get_store_by_id(store_id):
    conn = None
    try:
        conn = getCursor()
        query = """
        SELECT Store.store_id, Store.store_name, Store.address, Images.image_url
        FROM Store
        LEFT JOIN Images ON Store.image_id = Images.image_id
        WHERE Store.store_id = %s;
        """
        conn.execute(query, (store_id,))
        store = conn.fetchone()
        return store
    except Exception as e:
        print(f"Failed to retrieve store: {e}")
        return None
    finally:
        if conn:
            conn.close()


def update_store(store_id, store_name, address, image_id=None):
    conn = getCursor()
    try:
        updates = []
        parameters = [store_name, address, store_id]

        sql = "UPDATE Store SET store_name = %s, address = %s"

        if image_id:
            sql += ", image_id = %s"
            parameters.insert(2, image_id)  # Insert image_id before store_id in the parameters list

        sql += " WHERE store_id = %s"
        conn.execute(sql, parameters)
        conn.commit()
    except Exception as e:
        print(f"Failed to update store: {e}")
    finally:
        conn.close()


def get_all_stores_with_managers():
    conn = getCursor()
    query = """
    SELECT Store.store_id, Store.store_name, Store.address, Images.image_url, Local_Manager.first_name, Local_Manager.last_name, User.email FROM Store
    LEFT JOIN Local_Manager ON Store.store_id = Local_Manager.store_id
    LEFT JOIN User ON Local_Manager.user_id = User.user_id
    LEFT JOIN Images ON Store.image_id = Images.image_id;
    """
    conn.execute(query)
    stores = conn.fetchall()
    conn.close()

    return stores


def fetch_all_news():
    conn = getCursor()
    try:
        query = """
        SELECT news_id, title, content, posted_date, image_url, author_id
        FROM News
        JOIN Images ON News.image_id = Images.image_id
        ORDER BY posted_date DESC;
        """
        conn.execute(query)
        news_items = conn.fetchall() 
        return news_items
    except Exception as e:
        print(f"Error fetching news: {e}")
        return [] 
    finally:
        conn.close()  

def get_all_promotions():
    conn = getCursor()
    conn.execute("""SELECT DISTINCT p.*, e.name
                    FROM Promotions p
                    LEFT JOIN Sub_Category sub ON p.sub_category_id = sub.sub_category_id
                    LEFT JOIN Equipment e ON p.sub_category_id = e.sub_category_id
                    """)
    promotions = conn.fetchall()

    for promotion in promotions:
        promotion['start_date'] = format_date(promotion['start_date'])
        promotion['end_date'] = format_date(promotion['end_date'])
    
    conn.close

    return promotions

def add_promotion_item(title, equipment, image_id, description, start_date, end_date, discount_rate):
    conn = getCursor()
    conn.execute("INSERT INTO Promotions (title, sub_category_id, image_id, description, start_date, end_date, discount_rate) VALUES (%s, %s, %s, %s, %s, %s, %s)", (title, equipment, image_id, description, start_date, end_date, discount_rate))
    conn.close()

def get_promotion_by_promotion_id(promotion_id):
    conn = getCursor()
    conn.execute("""SELECT DISTINCT p.*, e.name, i.image_url, sub.sub_category_name
                    FROM Promotions p
                    LEFT JOIN Sub_Category sub ON p.sub_category_id = sub.sub_category_id
                    LEFT JOIN Equipment e ON p.sub_category_id = e.sub_category_id
                    LEFT JOIN Images i ON p.image_id = i.image_id
                    WHERE p.promotion_id = %s;
                    """, (promotion_id,))
    promotion = conn.fetchone()
    
    conn.close

    return promotion

def update_promotion(promotion_id, title, equipment, image_id, description, start_date, end_date, discount_rate):
    conn = getCursor()
    conn.execute("UPDATE Promotions SET title = %s, sub_category_id = %s, image_id = %s, description = %s, start_date = %s, end_date = %s, discount_rate = %s WHERE promotion_id = %s", (title, equipment, image_id, description, start_date, end_date, discount_rate, promotion_id))
    conn.close()

def remove_promotion(promotion_id):
    conn = getCursor()
    conn.execute("DELETE FROM Promotions WHERE promotion_id = %s", (promotion_id,))
    conn.close()

def get_message_by_id(message_id):
    conn = getCursor()
    conn.execute("""SELECT * FROM Messages 
                WHERE message_id = %s""", (message_id,))
    message = conn.fetchone()
    return message
    

def update_message_read_status(message_id):
    conn = getCursor()
    conn.execute("UPDATE Messages SET status = 'read', read_time = NOW() WHERE message_id = %s", (message_id,))
    conn.close()
    return '', 204  

def update_message_table_with_reply(message_id, sender_id, receive_id, store_id, subject, body_message, enquiry_message_id):
    conn = getCursor()
    query = """
    INSERT INTO Messages (
        sender_id, receiver_id, store_id, subject, message_text, status, response_message_id
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    conn.execute(query, (
        sender_id, 
        receive_id if receive_id else None, 
        store_id, 
        subject, 
        body_message, 
        'responded', 
        enquiry_message_id if enquiry_message_id else None
    ))
    conn.execute("UPDATE Messages SET status = 'responded' WHERE message_id = %s", (message_id,))

    conn.close()


def fetch_promotions():
    conn = getCursor()
    try:
        query = """
            SELECT p.*, sc.sub_category_name, i.image_url
        FROM Promotions p
        JOIN Sub_Category sc ON p.sub_category_id = sc.sub_category_id
        JOIN Images i ON p.image_id = i.image_id
        WHERE CURDATE() BETWEEN p.start_date AND p.end_date;
        """
        conn.execute(query)
        promotions = conn.fetchall()
        return promotions
    except Exception as e:
        print(f"Error fetching promotions: {e}")
        return []
    finally:
        conn.close()


def get_discounted_equipment():
    cursor = getCursor()
    query = """
    SELECT 
    subquery.equipment_id,
    subquery.name,
    subquery.sub_category_id,
    subquery.image_url,
    subquery.hire_cost,  
    subquery.discount_rate
    FROM (
        SELECT
            e.equipment_id,
            e.name,
            e.sub_category_id,
            i.image_url,
            sc.hire_cost,  
            p.discount_rate,
            ROW_NUMBER() OVER (PARTITION BY e.sub_category_id ORDER BY sc.hire_cost ASC) AS rn
        FROM Equipment e
        INNER JOIN Promotions p ON e.sub_category_id = p.sub_category_id
        INNER JOIN Sub_Category sc ON e.sub_category_id = sc.sub_category_id
        INNER JOIN Images i ON e.sub_category_id = i.sub_category_id AND i.entity_type = 'equipment'
        WHERE p.start_date <= CURDATE() AND p.end_date >= CURDATE()
        AND p.discount_rate > 0
    ) AS subquery
    WHERE subquery.rn = 1;
    """
    cursor.execute(query)
    discounted_equipment = cursor.fetchall()
    cursor.close()
    return discounted_equipment

def get_total_income():
    conn = getCursor()
    conn.execute("SELECT SUM(amount) AS total_amount FROM Payments WHERE YEAR(payment_date) = YEAR(CURRENT_DATE);")
    total_income = conn.fetchone()
    conn.close()

    return total_income

def get_total_expense():
    conn = getCursor()
    conn.execute("SELECT SUM(purchase_cost) AS total_expense FROM Equipment WHERE YEAR(purchase_date) = YEAR(CURRENT_DATE);")
    total_expense = conn.fetchone()
    conn.close()
    
    return total_expense

def get_total_income_for_store(store_id):
    conn = getCursor()
    conn.execute("""
                 SELECT SUM(total_amount) AS total_amount
                 FROM (
                        SELECT DISTINCT p.amount AS total_amount
                        FROM Payments p 
                        LEFT JOIN Orders o ON p.payment_id = o.payment_id
                        LEFT JOIN OrderBookings ob ON o.order_id = ob.order_id
                        LEFT JOIN Bookings b ON ob.booking_id = b.booking_id
                        LEFT JOIN Equipment e ON b.equipment_id = e.equipment_id     
                        WHERE e.store_id = %s 
                        AND YEAR(p.payment_date) = YEAR(CURRENT_DATE)
                           ) AS subquery;""",(store_id,))
    total_income = conn.fetchone()
    conn.close()

    return total_income

def get_total_expense_for_store(store_id):
    conn = getCursor()
    conn.execute("SELECT SUM(purchase_cost) AS total_expense FROM Equipment WHERE store_id = %s AND YEAR(purchase_date) = YEAR(CURRENT_DATE);", (store_id,))
    total_expense = conn.fetchone()
    conn.close()
    
    return total_expense

# Function to check for existing promotions
def check_existing_promotions(equipment_id, start_date, end_date, current_promotion_id=None):
    conn = getCursor()
    query = """
        SELECT COUNT(*) FROM Promotions
        WHERE sub_category_id = %s AND (
              (start_date <= %s AND end_date >= %s) OR
              (start_date <= %s AND end_date >= %s) OR
              (start_date >= %s AND end_date <= %s)
        )
    """
    params = [equipment_id, end_date, start_date, start_date, end_date, start_date, end_date]

    # Exclude the current promotion from the overlap check
    if current_promotion_id:
        query += " AND promotion_id != %s"
        params.append(current_promotion_id)

    conn.execute(query, tuple(params))
    result = conn.fetchone()
    return result['COUNT(*)'] > 0 

def retrieve_notifications(user_id):
    conn = getCursor()
    
    # First, retrieve all notifications for the user or for general notifications marked as '0'
    conn.execute("""
        SELECT 
            notification_id, 
            user_id, 
            message, 
            created_at, 
            TIMESTAMPDIFF(DAY, created_at, NOW()) AS days_ago
        FROM 
            Notifications
        WHERE 
            user_id = %s OR user_id IS NULL
        ORDER BY 
            notification_id DESC;
    """, (user_id,))
    notifications = conn.fetchall()

    # Convert 'days_ago' into a more readable format
    for notification in notifications:
        if notification['days_ago'] == 0:
            notification['time_ago'] = "Today"
        elif notification['days_ago'] == 1:
            notification['time_ago'] = "Yesterday"
        else:
            notification['time_ago'] = f"{notification['days_ago']} days ago"

    # Secondly, count today's messages separately
    conn.execute("""
        SELECT COUNT(*) AS count_today_message
        FROM Notifications
        WHERE (user_id = %s OR user_id IS NULL) AND DATE(created_at) = CURDATE();
    """, (user_id,))
    today_message_count_result = conn.fetchone()
    today_message_count = today_message_count_result['count_today_message'] if today_message_count_result else 0

    conn.close()  # Always ensure the connection is closed

    # Return both notifications and the count of today's messages
    return notifications, today_message_count

def retrieve_all_notifications():
    conn = getCursor()
    conn.execute("""SELECT 
                    N.notification_id, 
                    N.user_id, 
                    N.message, 
                    N.created_at, 
                    C.*,
                    TIMESTAMPDIFF(DAY, N.created_at, NOW()) AS time_ago,
                    (SELECT COUNT(*) 
                    FROM Notifications 
                    WHERE DATE(created_at) = CURDATE()) AS today_message_count
                    FROM 
                    Notifications N
                    LEFT JOIN Customer C ON N.user_id = C.user_id
                    ORDER BY 
                    N.created_at DESC;
                """)  
    notifications = conn.fetchall()

    # Humanize the 'days_ago' for better readability
    for notification in notifications:
        if notification['time_ago'] == 0:
            notification['time_ago'] = "Today"
        elif notification['time_ago'] == 1:
            notification['time_ago'] = "Yesterday"
        else:
            notification['time_ago'] = str(notification['time_ago']) + " days ago"
        notification['created_at'] = format_datetime(notification['created_at'])

    conn.close()  # Ensure the connection is closed after execution

    return notifications

def get_all_customer():
    conn = getCursor()
    conn.execute("""SELECT C.user_id, 
                    CONCAT(C.first_name, ' ', C.last_name) AS full_name
                    FROM Customer C;""")
    customers = conn.fetchall()
    return customers

def generate_notification(user_id, message):
    conn = getCursor()
    # Convert empty string to None for user_id if needed
    user_id = None if user_id == '' else user_id
    conn.execute("""INSERT INTO Notifications (user_id, message) VALUES (%s, %s)""", (user_id, message))
    conn.close()


def remove_notification(notification_id):
    conn = getCursor()
    conn.execute("DELETE FROM Notifications WHERE notification_id = %s", (notification_id,))
    conn.close()
def get_customers_count():
    conn = getCursor()
    conn.execute("SELECT COUNT(*) AS customer_count FROM Customer;")
    total_customers = conn.fetchone()
    conn.close()
    
    return total_customers

def get_orders_count():
    conn = getCursor()
    conn.execute("SELECT COUNT(*) AS orders_count FROM Orders;")
    total_orders = conn.fetchone()
    conn.close()
    
    return total_orders

def get_income_by_month():
    conn = getCursor()
    conn.execute("""
                 SELECT 
                     YEAR(payment_date) AS year,
                     MONTH(payment_date) AS month,
                     SUM(amount) AS total_amount
                 FROM 
                     Payments
                 WHERE
                     YEAR(payment_date) = YEAR(CURRENT_DATE)
                 GROUP BY 
                     YEAR(payment_date), MONTH(payment_date)
                 ORDER BY 
                     year, month;""")
    income_by_month = conn.fetchall()
    conn.close()
    
    return income_by_month
def get_expense_by_month():
    conn = getCursor()
    conn.execute("""
                   SELECT 
                      YEAR(purchase_date) AS year,
                      MONTH(purchase_date) AS month,
                      SUM(purchase_cost) AS total_purchase_cost
                   FROM 
                        Equipment
                   WHERE
                     YEAR(purchase_date) = YEAR(CURRENT_DATE)
                   GROUP BY 
                     YEAR(purchase_date), MONTH(purchase_date)
                   ORDER BY 
                     year, month;
                   """)
    expense_by_month = conn.fetchall()
    conn.close()
    
    return expense_by_month

def get_total_expense_for_store_by_month(store_id):
    conn = getCursor()
    conn.execute("""
                 SELECT
                      YEAR(purchase_date) AS year,
                      MONTH(purchase_date) AS month,
                      SUM(purchase_cost) AS total_purchase_cost
                 FROM
                      Equipment
                 WHERE
                       YEAR(purchase_date) = YEAR(CURRENT_DATE) AND store_id = %s
                 GROUP BY
                       YEAR(purchase_date),
                       MONTH(purchase_date);
                 """, (store_id,))
    total_monthly_expense = conn.fetchall()
    conn.close()
    
    return total_monthly_expense


def get_total_income_for_store_by_month(store_id):
    conn = getCursor()
    conn.execute("""
                    SELECT
                          YEAR(p.payment_date) AS year,
                          MONTH(p.payment_date) AS month,
                          SUM(p.amount) AS total_amount
                    FROM 
                           Payments p 
                    LEFT JOIN 
                           Orders o ON p.payment_id = o.payment_id
                    LEFT JOIN
                           OrderBookings ob ON o.order_id = ob.order_id
                    LEFT JOIN
                           Bookings b ON ob.booking_id = b.booking_id
                    LEFT JOIN
                           Equipment e ON b.equipment_id = e.equipment_id     
                    WHERE 
                           e.store_id = %s AND YEAR(p.payment_date) = YEAR(CURRENT_DATE)
                    GROUP BY
                           YEAR(p.payment_date),
                           MONTH(p.payment_date);""",(store_id,))
    total_monthly_income = conn.fetchall()
    conn.close()

    return total_monthly_income

def add_service_for_equipment(equipment_id, service_date, cost, description):
    conn = getCursor()
    query = """
    INSERT INTO Services (equipment_id, service_date, description, cost)
    VALUES (%s, %s, %s, %s)
    """
    conn.execute(query, (equipment_id, service_date, description, cost))
    conn.close()

def get_services_by_store_id(store_id):
    conn = getCursor()
    query = """
                SELECT e.store_id, s.* FROM Services s INNER JOIN Equipment e ON s.equipment_id = e.equipment_id
                WHERE e.store_id = %s;
                """
    conn.execute(query, (store_id,))
    services = conn.fetchall()
    return services

def get_return_time_for_equipment(equipment_id):
    conn = getCursor()
    conn.execute(""" SELECT MAX(return_datetime) AS latest_checkout_time FROM Bookings WHERE equipment_id= %s;""", (equipment_id,))
    result = conn.fetchone()
    if result and result['latest_checkout_time']:
        latest_checkout_time = result['latest_checkout_time']
        if isinstance(latest_checkout_time, str):
            latest_checkout_time = datetime.strptime(latest_checkout_time, '%Y-%m-%d %H:%M:%S')
        
        next_day = latest_checkout_time + timedelta(days=1)
        return next_day.date()
    return None

def is_service_date_within_booking_period(equipment_id, service_date):
    conn = getCursor()
    conn.execute("""
        SELECT COUNT(*) AS booking_count
        FROM Bookings
        WHERE equipment_id = %s
         AND (
            %s BETWEEN checkout_datetime AND return_datetime
         OR %s = DATE(checkout_datetime) OR %s = DATE(return_datetime));
    """, (equipment_id, service_date, service_date, service_date))
    result = conn.fetchone()
    return result['booking_count'] > 0



def get_shipping_count():
    conn = getCursor()
    conn.execute("SELECT count(*) AS shipping_count FROM Bookings WHERE YEAR(return_datetime) = YEAR(CURRENT_DATE);")
    total_shipping = conn.fetchone()
    conn.close()
    
    return total_shipping

def get_shipping_count_by_store(store_id):
    conn = getCursor()
    conn.execute("""SELECT count(*) AS shipping_count 
                    FROM Bookings b
                    LEFT JOIN Equipment e
                    ON b.equipment_id = e.equipment_id
                    WHERE store_id = %s AND YEAR(b.return_datetime) = YEAR(CURRENT_DATE);""",(store_id,))
    total_shipping = conn.fetchone()
    conn.close()
    
    return total_shipping

def get_booking_amount():
    conn = getCursor()
    conn.execute("SELECT SUM(line_total) as booking_amount FROM Bookings WHERE YEAR(return_datetime) = YEAR(CURRENT_DATE);")
    total_booking_amount = conn.fetchone()
    conn.close()
    
    return total_booking_amount

def get_booking_amount_by_store(store_id):
    conn = getCursor()
    conn.execute("""SELECT SUM(line_total) as booking_amount 
                    FROM Bookings b
                    LEFT JOIN Equipment e
                    ON b.equipment_id = e.equipment_id
                    WHERE store_id = %s AND YEAR(b.return_datetime) = YEAR(CURRENT_DATE);""",(store_id,))
    total_booking_amount = conn.fetchone()
    conn.close()
    
    return total_booking_amount

def get_orders_by_store(store_id):
    conn = getCursor()
    conn.execute("""SELECT COUNT(*) AS orders_count
                   FROM (
                         SELECT DISTINCT o.order_id
                         FROM Orders o 
                         LEFT JOIN OrderBookings ob ON o.order_id = ob.order_id
                         LEFT JOIN Bookings b ON ob.booking_id = b.booking_id
                         LEFT JOIN Equipment e ON b.equipment_id = e.equipment_id     
                         WHERE e.store_id = %s AND YEAR(o.order_date) = YEAR(CURRENT_DATE)
                         GROUP BY o.order_id  
                        ) AS subquery;""",(store_id,))
    order_count = conn.fetchone()
    conn.close()
    
    return order_count

def get_customer_by_store(store_id):
    
    conn = getCursor()
    conn.execute("""SELECT COUNT(*) AS customer_count
                    FROM (
                           SELECT DISTINCT c.customer_id
                           FROM Orders o 
                           LEFT JOIN Customer c ON o.customer_id = c.customer_id
                           LEFT JOIN OrderBookings ob ON o.order_id = ob.order_id
                           LEFT JOIN Bookings b ON ob.booking_id = b.booking_id
                           LEFT JOIN Equipment e ON b.equipment_id = e.equipment_id
                           WHERE e.store_id = %s) AS subquery;""",(store_id,))
    customer_count = conn.fetchone()
    conn.close()
    
    return customer_count

def get_all_available_equipment():
    conn = getCursor()
    conn.execute("""SELECT 
                       e.name,
                       COUNT(e.equipment_id) AS available_quantity,
                       s.store_name,
                       e.sub_category_id,
                       e.store_id
                    FROM 
                        Equipment e
                    LEFT JOIN Store s ON e.store_id = s.store_id
                    WHERE 
                        e.equipment_status = 'available'
                    GROUP BY 
                        e.name,
                        s.store_name,
                        e.sub_category_id,
                        e.store_id;
                       """)
    
    available_equipment = conn.fetchall()
    conn.close()
    
    return available_equipment

def get_available_equipment_by_store(store_id):
    conn = getCursor()
    conn.execute("""SELECT 
                    e.name,
                    COUNT(e.equipment_id) AS available_quantity,
                    s.store_name
                FROM 
                    Equipment e
                    INNER JOIN Store s ON e.store_id = s.store_id
                WHERE 
                    e.equipment_status = 'available'
                    AND s.store_id = %s
                GROUP BY 
                    e.name,
                    s.store_name;""",(store_id,))
    
    available_equipment = conn.fetchall()
    conn.close()
    
    return available_equipment

def get_all_orders():
    conn = getCursor()
    conn.execute("""SELECT o.order_id, p.payment_id, p.amount, p.payment_date, u.user_id, CONCAT(c.first_name, ' ', c.last_name) As customer_name, c.address, c.phone, u.email , o.order_date, o.payment_method, o.special_instruction, o.status
                    FROM Orders o
                    INNER JOIN Payments p ON p.payment_id = o.payment_id
                    INNER JOIN Customer c ON c.customer_id = o.customer_id
                    INNER JOIN User u ON c.user_id = u.user_id;""")
    orders = conn.fetchall()
   # Iterate through each row and format the order_date
    for order in orders:
        order['order_date'] = format_datetime(order['order_date'])
    return orders


def update_admin_profile(title, firstname, lastname, email, phone, address):
    conn = getCursor()
    conn.execute("UPDATE User SET email = %s WHERE user_id = %s", (email, session['user_id']))
    
    # Update the Admin details in the staff table
    conn.execute("UPDATE Administrator SET title = %s, first_name = %s, last_name = %s, phone = %s, address = %s WHERE user_id = %s",
                 (title, firstname, lastname, phone, address, session['user_id']))
    conn.close()
    
def get_admin_by_user_id(user_id):
    conn = getCursor()
  
    conn.execute("""SELECT u.*, a.* FROM User u
                LEFT JOIN Administrator a ON u.user_id = a.user_id WHERE u.user_id = %s""", (user_id,))
    user = conn.fetchone()
    return user

def get_local_manager():
    conn = getCursor()
    conn.execute("""SELECT u.*, l.* FROM Local_Manager l
                LEFT JOIN User u ON u.user_id = l.user_id""")
    users = conn.fetchall()
    return users

def get_national_manager():
    conn = getCursor()
    conn.execute("""SELECT u.*, n.* FROM National_Manager n
                LEFT JOIN User u ON u.user_id = n.user_id""")
    users = conn.fetchall()
    return users

def add_national_manager(title_id, email, firstname, lastname, phone, address, password):
    hashed_password = hash_password(password)
    conn = getCursor()
 
    # Insert the new user to db
    conn.execute("INSERT INTO User (email, password, role_id) VALUES (%s, %s, %s)", (email, hashed_password, 5))
    # Get the user id
    user_id = conn.lastrowid
    # Insert the new staff to db
    conn.execute("INSERT INTO National_Manager (user_id, title, first_name, last_name, phone, address) VALUES (%s, %s, %s, %s, %s, %s)", (user_id, title_id, firstname, lastname, phone, address,))
    conn.close
    
def delete_national_manager_sql(user_id):
    conn = getCursor()
    conn.execute("DELETE FROM National_Manager WHERE user_id = %s", (user_id,))
    conn.execute("DELETE FROM User WHERE user_id = %s", (user_id,))
    conn.close()
    
def update_national_manager_sql(title, firstname, lastname, email, phone, address,password,user_id):
    hashed_password = hash_password(password)
    conn = getCursor()
    conn.execute("UPDATE User SET email = %s, password = %s WHERE user_id = %s", (email, hashed_password, user_id,))
    
    # Update the national manager details in the national manager table
    conn.execute("UPDATE National_Manager SET title = %s, first_name = %s, last_name = %s, phone = %s, address = %s WHERE user_id = %s",
                 (title, firstname, lastname, phone, address, user_id,))
    conn.close()

def get_national_manager_details_by_user_id(user_id):
    conn = getCursor()
    conn.execute("""SELECT u.*, s.* FROM User u
                    LEFT JOIN National_Manager s ON u.user_id = s.user_id 
                    WHERE u.user_id = %s""", (user_id,))
    
    user = conn.fetchone()
    return user

def update_equipment_status(equipment_id):
    conn = getCursor()
    conn.execute("UPDATE Equipment SET equipment_status= 'removed' WHERE equipment_id= %s",(equipment_id,))
    conn.close()