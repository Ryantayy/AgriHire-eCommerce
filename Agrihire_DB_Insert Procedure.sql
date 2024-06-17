USE AgriHireDB;

DELIMITER $$

-- Create a stored procedure to insert dummy data into various tables
CREATE PROCEDURE insert_dummy_data()
BEGIN
  DECLARE i INT DEFAULT 1;
  DECLARE max_serial INT DEFAULT 0;
  DECLARE store_id INT DEFAULT 1;
  DECLARE sub_category_id INT DEFAULT 1;
  DECLARE new_serial VARCHAR(10);
  DECLARE duplicate_key INT DEFAULT 0;
  DECLARE category_name VARCHAR(30);
  DECLARE sub_category_name VARCHAR(255);

  -- Find the highest current serial number
  SELECT COALESCE(MAX(CAST(SUBSTRING(serial_number, 3) AS UNSIGNED)), 20) INTO max_serial FROM Equipment;

  -- Insert Equipment data and update Equipment_Stock table
  WHILE store_id <= 8 DO
    WHILE sub_category_id <= 21 DO
      -- Get category and subcategory names
      SELECT c.category_name, s.sub_category_name 
      INTO category_name, sub_category_name
      FROM Category c
      JOIN Sub_Category s ON c.category_id = s.category_id
      WHERE s.sub_category_id = sub_category_id;

      WHILE i <= 20 DO
        SET duplicate_key = 1;

        -- Loop to get unique serial number
        WHILE duplicate_key = 1 DO
          SET max_serial = max_serial + 1;
          SET new_serial = CONCAT('SN', LPAD(max_serial, 3, '0'));

          -- Insert the new record
          BEGIN
            DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
              SET duplicate_key = 1;

            INSERT INTO Equipment 
            (name, serial_number, category_id, sub_category_id, store_id, purchase_date, purchase_cost, equipment_condition, equipment_status) 
            VALUES 
            (CONCAT(category_name, ' - ', sub_category_name), new_serial,  
             (sub_category_id % 8) + 1, sub_category_id, store_id, '2023-05-10', 25000.00, 
             CASE 
               WHEN i % 5 = 0 THEN 'new' 
               WHEN i % 5 = 1 THEN 'good' 
               WHEN i % 5 = 2 THEN 'fair' 
               WHEN i % 5 = 3 THEN 'poor' 
               ELSE 'out_of_service' 
             END, 
             CASE 
               WHEN i % 4 = 0 THEN 'available' 
               WHEN i % 4 = 1 THEN 'hired' 
               WHEN i % 4 = 2 THEN 'unavailable' 
               ELSE 'removed' 
             END);

            -- If insert is successful, set duplicate_key to 0
            SET duplicate_key = 0;
          END;
        END WHILE;

        SET i = i + 1;
      END WHILE;
      INSERT INTO Equipment_Stock (store_id, sub_category_id, available_quantity) VALUES
      (store_id, sub_category_id, 20)
      ON DUPLICATE KEY UPDATE available_quantity = available_quantity + 20;
      SET i = 1;
      SET sub_category_id = sub_category_id + 1;
    END WHILE;
    SET sub_category_id = 1;
    SET store_id = store_id + 1;
  END WHILE;

  -- Insert Payments data
  SET i = 1;
  WHILE i <= 200 DO
    INSERT INTO Payments (amount, payment_date, user_id) 
    VALUES 
    ((i % 200) * 10.00, CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0'), ' ', LPAD(FLOOR(8 + RAND() * 10), 2, '0'), ':00:00'), (i % 10) + 1);
    SET i = i + 1;
  END WHILE;

  -- Insert Bookings data
  SET i = 1;
  SET store_id = 1;
  WHILE store_id <= 8 DO
    WHILE i <= 30 DO
      INSERT INTO Bookings (user_id, equipment_id, checkout_datetime, return_datetime, status, payment_id) 
      VALUES 
      ((i % 10) + 1, ((i % 20) + 1 + (store_id - 1) * 20), 
       CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0'), ' ', LPAD(FLOOR(8 + RAND() * 10), 2, '0'), ':00:00'), 
       CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0'), ' ', LPAD(FLOOR(8 + RAND() * 10), 2, '0'), ':00:00'), 
       CASE 
         WHEN i % 5 = 0 THEN 'booked' 
         WHEN i % 5 = 1 THEN 'pending' 
         WHEN i % 5 = 2 THEN 'checked_out' 
         WHEN i % 5 = 3 THEN 'returned' 
         ELSE 'cancelled' 
       END, (i % 200) + 1);
      SET i = i + 1;
    END WHILE;
    SET i = 1;
    SET store_id = store_id + 1;
  END WHILE;

  -- Insert Cart data
  SET i = 1;
  WHILE i <= 30 DO
    INSERT INTO Cart (user_id, equipment_id, checkout_datetime, return_datetime, quantity, total_cost) 
    VALUES 
    ((i % 10) + 1, (i % 20) + 1, 
     CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0'), ' ', LPAD(FLOOR(8 + RAND() * 10), 2, '0'), ':00:00'), 
     CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0'), ' ', LPAD(FLOOR(8 + RAND() * 10), 2, '0'), ':00:00'), 1, 
     (i % 1000) + 100.00),
    ((i % 10) + 1, (i % 20) + 2, 
     CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0'), ' ', LPAD(FLOOR(8 + RAND() * 10), 2, '0'), ':00:00'), 
     CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0'), ' ', LPAD(FLOOR(8 + RAND() * 10), 2, '0'), ':00:00'), 1, 
     (i % 1000) + 200.00),
    ((i % 10) + 1, (i % 20) + 3, 
     CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0'), ' ', LPAD(FLOOR(8 + RAND() * 10), 2, '0'), ':00:00'), 
     CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0'), ' ', LPAD(FLOOR(8 + RAND() * 10), 2, '0'), ':00:00'), 1, 
     (i % 1000) + 300.00),
    ((i % 10) + 1, (i % 20) + 4, 
     CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0'), ' ', LPAD(FLOOR(8 + RAND() * 10), 2, '0'), ':00:00'), 
     CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0'), ' ', LPAD(FLOOR(8 + RAND() * 10), 2, '0'), ':00:00'), 1, 
     (i % 1000) + 400.00),
    ((i % 10) + 1, (i % 20) + 5, 
     CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0'), ' ', LPAD(FLOOR(8 + RAND() * 10), 2, '0'), ':00:00'), 
     CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0'), ' ', LPAD(FLOOR(8 + RAND() * 10), 2, '0'), ':00:00'), 1, 
     (i % 1000) + 500.00);
    SET i = i + 1;
  END WHILE;

  -- Insert more Reviews data
  SET i = 1;
  WHILE i <= 150 DO
    INSERT INTO Reviews (booking_id, user_id, rating, comment) 
    VALUES 
    (i, (i % 10) + 1, (i % 5) + 1, 'Great service and equipment!'),
    (i + 1, (i % 10) + 1, (i % 5) + 1, 'Good experience overall.'),
    (i + 2, (i % 10) + 1, (i % 5) + 1, 'Average, could be better.'),
    (i + 3, (i % 10) + 1, (i % 5) + 1, 'Satisfied with the condition of the equipment.'),
    (i + 4, (i % 10) + 1, (i % 5) + 1, 'Highly recommend.');
    SET i = i + 5;
  END WHILE;

  -- Insert Services data to ensure each store has at least 20
  SET i = 1;
  SET store_id = 1;
  WHILE store_id <= 8 DO
    WHILE i <= 20 DO
      INSERT INTO Services (equipment_id, service_date, description, cost) 
      VALUES 
      ((i % 20) + 1 + (store_id - 1) * 20, CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0')), 'Routine maintenance.', 100.00),
      ((i % 20) + 2 + (store_id - 1) * 20, CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0')), 'Minor repairs.', 200.00),
      ((i % 20) + 3 + (store_id - 1) * 20, CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0')), 'Major overhaul.', 300.00),
      ((i % 20) + 4 + (store_id - 1) * 20, CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0')), 'Software update.', 400.00),
      ((i % 20) + 5 + (store_id - 1) * 20, CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0')), 'General checkup.', 500.00);
      SET i = i + 5;
    END WHILE;
    SET i = 1;
    SET store_id = store_id + 1;
  END WHILE;

  -- Insert Notifications data
  SET i = 1;
  WHILE i <= 150 DO
    INSERT INTO Notifications (user_id, message, created_at) 
    VALUES 
    ((i % 10) + 1, 'Your booking has been confirmed.', CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0'), ' 10:00:00')),
    ((i % 10) + 1, 'Reminder: Your booking ends soon.', CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0'), ' 11:00:00')),
    ((i % 10) + 1, 'Special promotion available!', CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0'), ' 12:00:00')),
    ((i % 10) + 1, 'Your payment has been received.', CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0'), ' 13:00:00')),
    ((i % 10) + 1, 'Thank you for your feedback!', CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0'), ' 14:00:00'));
    SET i = i + 5;
  END WHILE;

  -- Insert  Messages data
  SET i = 1;
  WHILE i <= 150 DO
    INSERT INTO Messages (sender_id, receiver_id, store_id, subject, message_text, sent_time, read_time, status) 
    VALUES 
    ((i % 10) + 1, 11, (i % 8) + 1, 'Inquiry about equipment', 'Can I get more details about the equipment?', CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0'), ' 10:00:00'), CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0'), ' 11:00:00'), 'read'),
    ((i % 10) + 1, 11, (i % 8) + 1, 'Booking confirmation', 'Please confirm my booking.', CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0'), ' 12:00:00'), CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0'), ' 13:00:00'), 'read'),
    ((i % 10) + 1, 11, (i % 8) + 1, 'Service request', 'I need to schedule a service for my equipment.', CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0'), ' 14:00:00'), CONCAT('2024-06-', LPAD(FLOOR(1 + RAND() * 5), 2, '0'), ' 15:00:00'), 'read');
    SET i = i + 3;
  END WHILE;
END$$

DELIMITER ;

-- Call the stored procedure to insert the dummy data
CALL insert_dummy_data();
