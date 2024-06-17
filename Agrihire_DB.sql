-- Create the Database
DROP DATABASE IF EXISTS AgriHireDB;
CREATE DATABASE IF NOT EXISTS AgriHireDB;
USE AgriHireDB;

CREATE TABLE IF NOT EXISTS Role (
	role_id INT PRIMARY KEY,
	role ENUM('customer', 'staff', 'local manager','administrator','national manager') NOT NULL
);


-- Create the main User Table
CREATE TABLE IF NOT EXISTS User (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    FOREIGN KEY (role_ID) REFERENCES Role(role_ID)
);


-- Create Images Table
CREATE TABLE IF NOT EXISTS Images (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    sub_category_id INT NOT NULL,
    entity_id INT NOT NULL,
    entity_type ENUM('equipment', 'staff', 'manager', 'customer', 'news','store', 'promotion') NOT NULL,
    image_url VARCHAR(255) NOT NULL
);


-- Create Locations Table
CREATE TABLE IF NOT EXISTS Store (
    store_id INT AUTO_INCREMENT PRIMARY KEY,
    store_name VARCHAR(200) NOT NULL,
    address VARCHAR(255) NOT NULL,
    image_id INT,  -- Reference to the image ID
    FOREIGN KEY (image_id) REFERENCES Images(image_id)
);
-- Create Customer Details Table
CREATE TABLE IF NOT EXISTS Customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    title VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(25) NOT NULL,
    address VARCHAR(255),
    date_of_birth DATE,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);



-- Create Staff Details Table
CREATE TABLE IF NOT EXISTS Staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    title VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(25),
    address VARCHAR(255),
    store_id INT NOT NULL,
    status BIT NOT NULL, 
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (store_id) REFERENCES Store(store_id)
);

-- Create Local Manager Details Table
CREATE TABLE IF NOT EXISTS Local_Manager (
    Local_manager_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    store_id INT,
    title VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(25) NOT NULL,
    address VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (store_id) REFERENCES Store(store_id)
);

-- Create Administrator Details Table
CREATE TABLE IF NOT EXISTS Administrator (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
	title VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(25) NOT NULL, 
    address VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

-- Create National Manager Details Table
CREATE TABLE IF NOT EXISTS National_Manager (
    national_manager_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    title VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    address VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);



-- Create Category Table
CREATE TABLE IF NOT EXISTS Category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(30) NOT NULL
);


-- Create the Sub_Category table
CREATE TABLE IF NOT EXISTS Sub_Category (
    sub_category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    sub_category_name VARCHAR(255) NOT NULL,
    hire_cost DECIMAL(10,2) NOT NULL,
    image_id INT NOT NULL,
    description TEXT,
    weight INT, 
    dimension VARCHAR(20),
    shipping_price DECIMAL(10, 2) DEFAULT 0.00,
    min_hire_period INT DEFAULT 1,
    max_hire_period INT DEFAULT 30,
    FOREIGN KEY (category_id) REFERENCES Category(category_id),
    FOREIGN KEY (image_id) REFERENCES Images(image_id)
);



-- Create Equipment Table
CREATE TABLE IF NOT EXISTS Equipment (
    equipment_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    serial_number VARCHAR(255) UNIQUE NOT NULL,
    category_id INT NOT NULL,
    sub_category_id INT NOT NULL,
    store_id INT NOT NULL,
    purchase_date DATE NOT NULL,
    purchase_cost DECIMAL(10,2) NOT NULL,
    equipment_condition ENUM('new', 'good', 'fair', 'poor', 'out_of_service') NOT NULL,
    equipment_status ENUM('available', 'unavailable', 'removed') NOT NULL,
    FOREIGN KEY (store_id) REFERENCES Store(store_id),
    FOREIGN KEY (category_id) REFERENCES Category(category_id),
    FOREIGN KEY (sub_category_id) REFERENCES Sub_Category(sub_category_id)
);


CREATE TABLE IF NOT EXISTS Equipment_Stock (
    store_id INT NOT NULL,
    sub_category_id INT NOT NULL,
    available_quantity INT NOT NULL,
    PRIMARY KEY (store_id, sub_category_id),
    FOREIGN KEY (sub_category_id) REFERENCES Sub_Category(sub_category_id)
);

-- Create Payments Table
CREATE TABLE IF NOT EXISTS Payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    amount DECIMAL(10,2) NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT,
    status ENUM('processed', 'cancelled') NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

-- Create Bookings Table
CREATE TABLE IF NOT EXISTS Bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    equipment_id INT NOT NULL,
    checkout_datetime DATETIME NOT NULL,
    return_datetime DATETIME NOT NULL,
    status ENUM('booked', 'pending', 'checked_out', 'returned', 'cancelled') NOT NULL,
    line_total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (equipment_id) REFERENCES Equipment(equipment_id)
);

DELIMITER //

CREATE EVENT IF NOT EXISTS update_booking_to_checked_out
ON SCHEDULE EVERY 1 MINUTE
DO
  BEGIN
    UPDATE Bookings
    SET status = 'checked_out'
    WHERE NOW() >= checkout_datetime
      AND status IN ('booked', 'pending');
  END//

DELIMITER ;

DELIMITER //
CREATE EVENT IF NOT EXISTS update_booking_to_returned
ON SCHEDULE EVERY 1 MINUTE
DO
  BEGIN
    UPDATE Bookings
    SET status = 'returned'
    WHERE NOW() >= return_datetime
      AND status = 'checked_out';
  END//

DELIMITER ;

-- Create Order Table
CREATE TABLE IF NOT EXISTS Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    shipping_address VARCHAR(255) NOT NULL,
    special_instruction TEXT,
    payment_method VARCHAR(100),
    customer_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	payment_id INT,
    status ENUM('confirmed', 'cancelled') NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
	FOREIGN KEY (payment_id) REFERENCES Payments(payment_id)
);

-- Create OrderBookings Table
CREATE TABLE IF NOT EXISTS OrderBookings (
    orderBooking_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    booking_id INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id)
);

-- Create Cart Table
CREATE TABLE IF NOT EXISTS Cart (
    cart_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    equipment_id INT NOT NULL,
	checkout_datetime DATETIME NOT NULL,
    return_datetime DATETIME NOT NULL,
    quantity INT NOT NULL,
    total_cost DECIMAL(10,2) NOT NULL, 
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (equipment_id) REFERENCES Equipment(equipment_id)
);

-- Create Reviews Table
CREATE TABLE IF NOT EXISTS Reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    user_id INT NOT NULL,
    rating INT NOT NULL,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

-- Create Services Table
CREATE TABLE IF NOT EXISTS Services (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    equipment_id INT,
    service_date DATE,
    description TEXT,
    cost DECIMAL(10,2),
    FOREIGN KEY (equipment_id) REFERENCES Equipment(equipment_id)
);

-- Create Promotions Table
CREATE TABLE IF NOT EXISTS Promotions (
    promotion_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    sub_category_id INT,
    image_id INT NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    discount_rate DECIMAL(5,2),
FOREIGN KEY (sub_category_id) REFERENCES Sub_Category(sub_category_id)
);


-- Create Notifications Table
CREATE TABLE IF NOT EXISTS Notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

CREATE TABLE IF NOT EXISTS News (
    news_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    image_id INT, 
    author_id INT,       
    FOREIGN KEY (author_id) REFERENCES User(user_id)  -- Assuming authors are users in your system
);

CREATE TABLE IF NOT EXISTS Messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT NOT NULL,
    receiver_id INT,
    serial_number VARCHAR(255) NULL,
    store_id INT NOT NULL,
    subject VARCHAR(255),
    message_text TEXT NOT NULL,
    sent_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_time TIMESTAMP NULL,
    response_message_id INT NULL,
    status ENUM('unread', 'read', 'responded') DEFAULT 'unread',
    FOREIGN KEY (sender_id) REFERENCES User(user_id),
    FOREIGN KEY (receiver_id) REFERENCES User(user_id),
    FOREIGN KEY (serial_number) REFERENCES Equipment(serial_number),
    FOREIGN KEY (store_id) REFERENCES Store(store_id)
); 

-- Create Customer Balances Table 
/* CREATE TABLE IF NOT EXISTS Customer_Balances (
    customer_id INT UNIQUE NOT NULL,
    balance DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
); */


CREATE TABLE IF NOT EXISTS PaymentMethods (
    card_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    card_type VARCHAR(20) NOT NULL, 
	name_on_card VARCHAR(20) NOT NULL,
    expiration_month VARCHAR(2) NOT NULL,
    expiration_year VARCHAR(2) NOT NULL,
    digits VARCHAR(20) NOT NULL,
    security_code VARCHAR(5) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
); 




