-- Insert data into Category table
INSERT INTO Category (category_id, category_name) VALUES
(1, 'tractors'),
(2, 'cultivation machinery'),
(3, 'feed mixers'),
(4, 'diggers'),
(5, 'lawn mowers'),
(6, 'sprayers'),
(7, 'chainsaws'),
(8, 'fence post drivers');

-- Insert data into Images table
INSERT INTO Images (sub_category_id, entity_id, entity_type, image_url) VALUES
(1, 1, 'equipment', 'tractor1a.png'),
(2, 1, 'equipment', 'tractor2a.png'),
(3, 1, 'equipment', 'tractor3a.png');


INSERT INTO Images (sub_category_id, entity_id, entity_type, image_url) VALUES
(4, 1, 'equipment', 'cultivator1a.png'),
(5, 1, 'equipment', 'cultivator2a.png'),
(6, 1, 'equipment', 'cultivator3a.png');


INSERT INTO Images (sub_category_id, entity_id, entity_type, image_url) VALUES
(7, 1, 'equipment', 'feedmixer1a.png'),
(8, 1, 'equipment', 'feedmixer2a.png'),
(9, 1, 'equipment', 'feedmixer3a.png');


INSERT INTO Images (sub_category_id, entity_id, entity_type, image_url) VALUES
(10, 1, 'equipment', 'digger1a.png'),
(11, 1, 'equipment', 'digger2a.png'),
(12, 1, 'equipment', 'digger3a.png');


INSERT INTO Images (sub_category_id, entity_id, entity_type, image_url) VALUES
(13, 1, 'equipment', 'lawnmower1a.png'),
(14, 1, 'equipment', 'lawnmower2a.png'),
(15, 1, 'equipment', 'lawnmower3a.png');


INSERT INTO Images (sub_category_id, entity_id, entity_type, image_url) VALUES
(16, 1, 'equipment', 'sprayer1a.png'),
(17, 1, 'equipment', 'sprayer2a.png'),
(18, 1, 'equipment', 'sprayer3a.png');


INSERT INTO Images (sub_category_id, entity_id, entity_type, image_url) VALUES
(19, 1, 'equipment', 'chainsaw1a.png'),
(20, 1, 'equipment', 'chainsaw2a.png'),
(21, 1, 'equipment', 'chainsaw3a.png');


INSERT INTO Images (sub_category_id, entity_id, entity_type, image_url) VALUES
(0, 6, 'store', 'stores-logo-1.svg'),
(0, 6, 'store', 'stores-logo-2.svg'),
(0, 6, 'store', 'stores-logo-3.svg'),
(0, 6, 'store', 'stores-logo-4.svg'),
(0, 6, 'store', 'stores-logo-5.svg'),
(0, 6, 'store', 'stores-logo-6.svg'),
(0, 6, 'store', 'stores-logo-7.svg'),
(0, 6, 'store', 'stores-logo-8.svg');


-- Insert News-related Images into the Images table with a single entity_id
INSERT INTO Images (sub_category_id, entity_id, entity_type, image_url) VALUES
(0, 5, 'news', 'news-lease.png'),
(0, 5, 'news', 'news-partnership.png'),
(0, 5, 'news', 'news-smarttech.png'),
(0, 5, 'news', 'news-tractor.png'),
(0, 5, 'news', 'news-newfleet.png');


-- Insert Promotion-related Images into the Images table
INSERT INTO Images (sub_category_id, entity_id, entity_type, image_url) VALUES
(0, 7, 'promotion', 'promo-tractors-spring.png'),
(0, 7, 'promotion', 'promo-cultivation-discount.png'),
(0, 7, 'promotion', 'promo-lawnmower-weekend.png');


-- Insert data into Sub_Category table
INSERT INTO Sub_Category (category_id, sub_category_name, hire_cost, image_id, description, weight, dimension, shipping_price, min_hire_period, max_hire_period) VALUES
(1, 'Tractor - John Deere 5100', 200.00, 1, 'High power tractor for heavy-duty tasks.', 2000, '3x2x2.5m', 150.00, 1, 30),
(1, 'Tractor - Kubota M7060', 190.00, 2, 'Efficient tractor with excellent fuel economy.', 1950, '3x2x2.3m', 145.00, 1, 30),
(1, 'Tractor - New Holland T7', 210.00, 3, 'Robust tractor with advanced hydraulics.', 2050, '3.1x2.1x2.6m', 155.00, 1, 30),
(2, 'Cultivator - Field King', 80.00, 4, 'High-performance cultivator for soil preparation.', 1100, '2.5x1.8x1.5m', 100.00, 1, 30),
(2, 'Cultivator - Great Plains Spartan II', 85.00, 5, 'Durable cultivator with adjustable depth settings.', 1150, '2.6x1.9x1.6m', 105.00, 1, 30),
(2, 'Cultivator - Land Pride APS1548', 75.00, 6, 'Compact cultivator ideal for small farms.', 1080, '2.4x1.7x1.4m', 95.00, 1, 30),
(3, 'Feed Mixer - Supreme 900T', 120.00, 7, 'Efficient feed mixer for various feed types.', 1300, '2x1.5x1.2m', 110.00, 1, 30),
(3, 'Feed Mixer - Kuhn Knight 3142', 125.00, 8, 'Feed mixer with customizable mixing blades.', 1350, '2.1x1.6x1.3m', 115.00, 1, 30),
(3, 'Feed Mixer - Penta 8030', 115.00, 9, 'Portable feed mixer with easy operation.', 1280, '1.9x1.4x1.1m', 105.00, 1, 30),
(4, 'Digger - Caterpillar 330', 300.00, 10, 'Heavy-duty digger for excavation tasks.', 4500, '4x3x3.5m', 200.00, 1, 30),
(4, 'Digger - Digger - Komatsu PC200', 290.00, 11, 'Compact digger for urban construction sites.', 4400, '3.9x2.9x3.4m', 190.00, 1, 30),
(4, 'John Deere 50G', 310.00, 12, 'Digger with enhanced digging depth and power.', 4600, '4.1x3.1x3.6m', 210.00, 1, 30),
(5, 'Honda HRX217VKA', 25.00, 13, 'Efficient lawn mower for large gardens.', 40, '1x0.5x0.85m', 20.00, 1, 30),
(5, 'Toro TimeMaster', 27.00, 14, 'Lawn mower with variable speed settings.', 45, '1.1x0.55x0.9m', 22.00, 1, 30),
(5, 'Husqvarna LC221RH', 23.00, 15, 'Compact lawn mower, easy to handle and store.', 35, '0.9x0.45x0.8m', 18.00, 1, 30),
(6, 'John Deere R4023', 30.00, 16, 'High-capacity sprayer for extensive agricultural fields.', 250, '1.5x1x1.2m', 30.00, 1, 30),
(6, 'Hardi Navigator 4000', 32.00, 17, 'Portable sprayer with adjustable nozzles.', 260, '1.6x1.1x1.3m', 35.00, 1, 30),
(6, 'Amazone UX5200', 28.00, 18, 'Eco-friendly sprayer, low chemical usage.', 240, '1.4x0.9x1.1m', 25.00, 1, 30),
(7, 'Stihl MS 250', 15.00, 19, 'Powerful chainsaw for heavy tree cutting.', 18, '0.8x0.2x0.3m', 10.00, 1, 30),
(7, 'Husqvarna 455 Rancher', 17.00, 20, 'Lightweight chainsaw, easy to handle and operate.', 16, '0.75x0.18x0.25m', 8.00, 1, 30),
(7, 'Echo CS-590', 12.00, 21, 'Chainsaw with extended battery life for longer use.', 20, '0.82x0.22x0.32m', 12.00, 1, 30);


-- Insert data into Store table
INSERT INTO Store (store_name, address, image_id) VALUES
('AgriHire Hamilton', '123 Hobsonville Road, Hamilton', 22),
('AgriHire Wellington', '456 Wellington Street, Wellington', 23),
('AgriHire Auckland', '789 Auckland Road, Auckland', 24),
('AgriHire Christchurch', '321 Christchurch Lane, Christchurch', 25),
('AgriHire Hamilton', '654 Hamilton Boulevard, Hamilton', 26),
('AgriHire Dunedin', '987 Dunedin Crescent, Dunedin', 27),
('AgriHire Tauranga', '135 Tauranga Drive, Tauranga', 28),
('AgriHire Napier', '246 Napier Road, Napier', 29);



-- Inser data into role
INSERT INTO Role (role_id, role) VALUES
(1, 'customer'),
(2, 'staff'),
(3, 'local manager'),
(4, 'administrator'),
(5, 'national manager');


-- Inserting data into User table for customer 
INSERT INTO User (email, password, role_id) VALUES
('ray@gmail.com', '9773a4fc863aa52c278186a2fb4a6391ebf50cd3fea9ea51ac3253bb6e3e07bb', 1),
('zac@gmail.com', '9773a4fc863aa52c278186a2fb4a6391ebf50cd3fea9ea51ac3253bb6e3e07bb', 1),
('rara@gmail.com', '9773a4fc863aa52c278186a2fb4a6391ebf50cd3fea9ea51ac3253bb6e3e07bb', 1),
('angela@gmail.com', '9773a4fc863aa52c278186a2fb4a6391ebf50cd3fea9ea51ac3253bb6e3e07bb', 1),
('lina@gmail.com', '9773a4fc863aa52c278186a2fb4a6391ebf50cd3fea9ea51ac3253bb6e3e07bb', 1),
('lulu@gmail.com', '9773a4fc863aa52c278186a2fb4a6391ebf50cd3fea9ea51ac3253bb6e3e07bb', 1),
('coco@gmail.com', '9773a4fc863aa52c278186a2fb4a6391ebf50cd3fea9ea51ac3253bb6e3e07bb', 1),
('cici@gmail.com', '9773a4fc863aa52c278186a2fb4a6391ebf50cd3fea9ea51ac3253bb6e3e07bb', 1),
('fafa@gmail.com', '9773a4fc863aa52c278186a2fb4a6391ebf50cd3fea9ea51ac3253bb6e3e07bb', 1),
('haha@gmail.com', '9773a4fc863aa52c278186a2fb4a6391ebf50cd3fea9ea51ac3253bb6e3e07bb', 1);

-- Insert data into User table for Staff and Managers
INSERT INTO User (email, password, role_id) VALUES
('john.doe@gmail.com', '9773a4fc863aa52c278186a2fb4a6391ebf50cd3fea9ea51ac3253bb6e3e07bb', 2),  -- Staff
('jane.smith@gmail.com', '9773a4fc863aa52c278186a2fb4a6391ebf50cd3fea9ea51ac3253bb6e3e07bb', 2),  -- Staff
('alice.johnson@gmail.com', '9773a4fc863aa52c278186a2fb4a6391ebf50cd3fea9ea51ac3253bb6e3e07bb', 2),  -- Staff
('bob.brown@gmail.com', '9773a4fc863aa52c278186a2fb4a6391ebf50cd3fea9ea51ac3253bb6e3e07bb', 2),  -- Staff
('charlie.davis@gmail.com', '9773a4fc863aa52c278186a2fb4a6391ebf50cd3fea9ea51ac3253bb6e3e07bb', 2),  -- Staff
('diana.clark@gmail.com', '9773a4fc863aa52c278186a2fb4a6391ebf50cd3fea9ea51ac3253bb6e3e07bb', 2),  -- Staff
('eva.lopez@gmail.com', '9773a4fc863aa52c278186a2fb4a6391ebf50cd3fea9ea51ac3253bb6e3e07bb', 2),  -- Staff
('frank.wilson@gmail.com', '9773a4fc863aa52c278186a2fb4a6391ebf50cd3fea9ea51ac3253bb6e3e07bb', 2),  -- Staff
('george.hill@gmail.com', '9773a4fc863aa52c278186a2fb4a6391ebf50cd3fea9ea51ac3253bb6e3e07bb', 3),  -- Manager
('hannah.martin@gmail.com', '9773a4fc863aa52c278186a2fb4a6391ebf50cd3fea9ea51ac3253bb6e3e07bb', 3),  -- Manager
('ivy.lee@gmail.com', '9773a4fc863aa52c278186a2fb4a6391ebf50cd3fea9ea51ac3253bb6e3e07bb', 3),  -- Manager
('jack.taylor@gmail.com', '9773a4fc863aa52c278186a2fb4a6391ebf50cd3fea9ea51ac3253bb6e3e07bb', 3),  -- Manager
('kevin.anderson@gmail.com', '9773a4fc863aa52c278186a2fb4a6391ebf50cd3fea9ea51ac3253bb6e3e07bb', 3),  -- Manager
('lily.moore@gmail.com', '9773a4fc863aa52c278186a2fb4a6391ebf50cd3fea9ea51ac3253bb6e3e07bb', 3),  -- Manager
('molly.thomas@gmail.com', '9773a4fc863aa52c278186a2fb4a6391ebf50cd3fea9ea51ac3253bb6e3e07bb', 5),  -- national Manager
('nathan.jackson@gmail.com', '9773a4fc863aa52c278186a2fb4a6391ebf50cd3fea9ea51ac3253bb6e3e07bb', 4);  -- Admin



INSERT INTO Customer (user_id, title, first_name, last_name, phone, address, date_of_birth) VALUES 
(1, 'Mr', 'Ray', 'La', '1234567890', '123 Main St', '1995-05-05'),
(2, 'Mrs', 'Zac', 'Smith', '9876543210', '456 Oak St', '1995-10-10'),
(3, 'Mr', 'Rara', 'Lee', '5551234567', '789 Elm St', '1988-03-15'),
(4, 'Miss', 'Angela', 'Brown', '3334445555', '321 Pine St', '1995-12-20'),
(5, 'Dr', 'Lina', 'Williams', '1112223333', '555 Cedar St', '1975-08-25'),
(6, 'Ms', 'Lulu', 'Taylor', '6667778888', '777 Maple St', '1983-07-12'),
(7, 'Mr', 'Coco', 'Anderson', '9998887777', '888 Birch St', '1992-01-30'),
(8, 'Mrs', 'Cici', 'Martinez', '4445556666', '999 Spruce St', '1970-11-05'),
(9, 'Miss', 'Fafa', 'Garcia', '2223334444', '222 Walnut St', '1980-04-18'),
(10, 'Mr', 'Haha', 'Hernandez', '7778889999', '333 Ash St', '1987-09-08');


-- Insert data into Staff table 
INSERT INTO Staff (user_id, title, first_name, last_name, phone, address, store_id, status) VALUES
(11, 'Mr', 'John', 'Doe', '0212345678', '123 Lane St, Wellington', 2, b'1'),
(12, 'Mrs', 'Jane', 'Smith', '0212345679', '456 Lane St, Auckland', 1, b'1'),
(13, 'Ms', 'Alice', 'Johnson', '0212345680', '789 Lane St, Christchurch', 3, b'1'),
(14, 'Dr', 'Bob', 'Brown', '0212345681', '321 Lane St, Hamilton', 4, b'1'),
(15, 'Mr', 'Charlie', 'Davis', '0212345682', '654 Lane St, Dunedin', 5, b'1'),
(16, 'Mrs', 'Diana', 'Clark', '0212345683', '987 Lane St, Tauranga', 6, b'1'),
(17, 'Ms', 'Eva', 'Lopez', '0212345684', '135 Lane St, Napier', 7, b'1'),
(18, 'Mr', 'Frank', 'Wilson', '0212345685', '246 Lane St, Hobsonville', 8, b'1');

-- Insert data into local_Manager table 
INSERT INTO Local_Manager (user_id, store_id, title, first_name, last_name, phone, address) VALUES
(19, 1, 'Mr', 'George', 'Hill', '0212345686', '123 Hill St, Wellington'),
(20, 2, 'Mrs', 'Hannah', 'Martin', '0212345687', '456 Hill St, Auckland'),
(21, 3, 'Ms', 'Ivy', 'Lee', '0212345688', '789 Hill St, Christchurch'),
(22, 4, 'Dr', 'Jack', 'Taylor', '0212345689', '321 Hill St, Hamilton'),
(23, 5, 'Mr', 'Kevin', 'Anderson', '0212345690', '654 Hill St, Dunedin'),
(24, 6, 'Mrs', 'Lily', 'Moore', '0212345691', '987 Hill St, Tauranga');


-- Insert data into national_Manager table 
INSERT INTO National_Manager (user_id, title, first_name, last_name, phone, address) VALUES
(25, 'Ms', 'Molly', 'Thomas', '0212345692', '135 Hill St, Napier');


-- Insert data into Administrator table 
INSERT INTO Administrator (user_id, title, first_name, last_name, phone, address) VALUES
(26, 'Mr', 'Nathan', 'Jackson', '0212345693', '246 Hill St, Hobsonville');



-- Insert data into Equipment table with new sub_category_id
INSERT INTO Equipment 
(name, serial_number, category_id, sub_category_id, store_id, purchase_date, purchase_cost, equipment_condition, equipment_status) VALUES
('Tractor - John Deere 5100', 'SN001', 1, 1, 1, '2023-05-10', 25000.00, 'new', 'available'),
('Tractor - John Deere 5100', 'SN001A', 1, 1, 1, '2023-05-10', 25000.00, 'new', 'available'),
('Tractor - John Deere 5100', 'SN001B', 1, 1, 2, '2023-05-10', 25000.00, 'new', 'available'),
('Tractor - Kubota M7060', 'SN002', 1, 2, 2, '2023-06-15', 24000.00, 'new', 'available'),
('Tractor - New Holland T7', 'SN003', 1, 3, 3, '2023-07-20', 26000.00, 'new', 'available'),
('Cultivator - Field King', 'SN004', 2, 4, 1, '2023-08-25', 8000.00, 'good', 'available'),
('Cultivator - Great Plains Spartan II', 'SN005', 2, 5, 2, '2023-09-30', 8200.00, 'good', 'available'),
('Cultivator - Land Pride APS1548', 'SN006', 2, 6, 3, '2023-10-05', 7900.00, 'good', 'available'),
('Feed Mixer - Supreme 900T', 'SN007', 3, 7, 1, '2023-11-10', 15000.00, 'new', 'available'),
('Feed Mixer - Kuhn Knight 3142', 'SN008', 3, 8, 2, '2023-12-15', 15200.00, 'new', 'available'),
('Feed Mixer - Penta 8030', 'SN009', 3, 9, 3, '2024-01-20', 14800.00, 'new', 'available'),
('Digger - Caterpillar 330', 'SN010', 4, 10, 1, '2024-02-25', 35000.00, 'new', 'available'),
('Digger - Komatsu PC200', 'SN011', 4, 11, 2, '2024-03-30', 34000.00, 'new', 'available'),
('Digger - John Deere 50G', 'SN012', 4, 12, 3, '2024-04-04', 36000.00, 'new', 'available'),
('Lawn Mower - Honda HRX217VKA', 'SN013', 5, 13, 1, '2023-05-10', 500.00, 'good', 'available'),
('Lawn Mower - Toro TimeMaster', 'SN014', 5, 14, 2, '2023-06-15', 550.00, 'good', 'available'),
('Lawn Mower - Husqvarna LC221RH', 'SN015', 5, 15, 3, '2023-07-20', 450.00, 'good', 'available'),
('Sprayer - John Deere R4023', 'SN016', 6, 16, 1, '2023-08-25', 3000.00, 'new', 'available'),
('Sprayer - Hardi Navigator 4000', 'SN017', 6, 17, 2, '2023-09-30', 3200.00, 'new', 'available'),
('Sprayer - Amazone UX5200', 'SN018', 6, 18, 3, '2023-10-05', 2800.00, 'new', 'available'),
('Chainsaw - Stihl MS 250', 'SN019', 7, 19, 1, '2023-11-10', 800.00, 'new', 'available'),
('Chainsaw - Husqvarna 455 Rancher', 'SN020', 7, 20, 2, '2023-12-15', 850.00, 'new', 'available'),
('Chainsaw - Echo CS-590', 'SN021', 7, 21, 3, '2024-01-20', 780.00, 'new', 'available');

-- Insert Equipment data
INSERT INTO Equipment (name, serial_number, category_id, sub_category_id, store_id, purchase_date, purchase_cost, equipment_condition, equipment_status) VALUES
('Tractor - John Deere 5100', 'SN2000', 1, 1, 1, '2023-05-10', 25000.00, 'new', 'available'),
('Tractor - John Deere 5100', 'SN2001', 1, 1, 1, '2023-05-10', 25000.00, 'new', 'available'),
('Tractor - John Deere 5100', 'SN2002', 1, 1, 1, '2023-05-10', 25000.00, 'good', 'unavailable'),
('Tractor - John Deere 5100', 'SN2003', 1, 1, 1, '2023-05-10', 25000.00, 'fair', 'removed'),
('Tractor - John Deere 5100', 'SN2004', 1, 1, 1, '2023-05-10', 25000.00, 'poor', 'available'),
('Tractor - Kubota M7060', 'SN2005', 1, 2, 1, '2023-06-15', 24000.00, 'new', 'available'),
('Tractor - Kubota M7060', 'SN2006', 1, 2, 1, '2023-06-15', 24000.00, 'new', 'available'),
('Tractor - Kubota M7060', 'SN2007', 1, 2, 1, '2023-06-15', 24000.00, 'good', 'unavailable'),
('Tractor - Kubota M7060', 'SN2008', 1, 2, 1, '2023-06-15', 24000.00, 'fair', 'removed'),
('Tractor - Kubota M7060', 'SN2009', 1, 2, 1, '2023-06-15', 24000.00, 'poor', 'available'),
('Tractor - New Holland T7', 'SN2010', 1, 3, 1, '2023-07-20', 26000.00, 'new', 'available'),
('Tractor - New Holland T7', 'SN2011', 1, 3, 1, '2023-07-20', 26000.00, 'new', 'available'),
('Tractor - New Holland T7', 'SN2012', 1, 3, 1, '2023-07-20', 26000.00, 'good', 'unavailable'),
('Tractor - New Holland T7', 'SN2013', 1, 3, 1, '2023-07-20', 26000.00, 'fair', 'removed'),
('Tractor - New Holland T7', 'SN2014', 1, 3, 1, '2023-07-20', 26000.00, 'poor', 'available'),
('Cultivator - Field King', 'SN2015', 2, 4, 1, '2023-08-25', 8000.00, 'new', 'available'),
('Cultivator - Field King', 'SN2016', 2, 4, 1, '2023-08-25', 8000.00, 'new', 'available'),
('Cultivator - Field King', 'SN2017', 2, 4, 1, '2023-08-25', 8000.00, 'good', 'unavailable'),
('Cultivator - Field King', 'SN2018', 2, 4, 1, '2023-08-25', 8000.00, 'fair', 'removed'),
('Cultivator - Field King', 'SN2019', 2, 4, 1, '2023-08-25', 8000.00, 'poor', 'available'),
('Cultivator - Great Plains Spartan II', 'SN2020', 2, 5, 1, '2023-09-30', 8200.00, 'new', 'available'),
('Cultivator - Great Plains Spartan II', 'SN2021', 2, 5, 1, '2023-09-30', 8200.00, 'new', 'available'),
('Cultivator - Great Plains Spartan II', 'SN2022', 2, 5, 1, '2023-09-30', 8200.00, 'good', 'unavailable'),
('Cultivator - Great Plains Spartan II', 'SN2023', 2, 5, 1, '2023-09-30', 8200.00, 'fair', 'removed'),
('Cultivator - Great Plains Spartan II', 'SN2024', 2, 5, 1, '2023-09-30', 8200.00, 'poor', 'available'),
('Cultivator - Land Pride APS1548', 'SN2025', 2, 6, 1, '2023-10-05', 7900.00, 'new', 'available'),
('Cultivator - Land Pride APS1548', 'SN2026', 2, 6, 1, '2023-10-05', 7900.00, 'new', 'available'),
('Cultivator - Land Pride APS1548', 'SN2027', 2, 6, 1, '2023-10-05', 7900.00, 'good', 'unavailable'),
('Cultivator - Land Pride APS1548', 'SN2028', 2, 6, 1, '2023-10-05', 7900.00, 'fair', 'removed'),
('Cultivator - Land Pride APS1548', 'SN2029', 2, 6, 1, '2023-10-05', 7900.00, 'poor', 'available'),
('Feed Mixer - Supreme 900T', 'SN2030', 3, 7, 1, '2023-11-10', 15000.00, 'new', 'available'),
('Feed Mixer - Supreme 900T', 'SN2031', 3, 7, 1, '2023-11-10', 15000.00, 'new', 'available'),
('Feed Mixer - Supreme 900T', 'SN2032', 3, 7, 1, '2023-11-10', 15000.00, 'good', 'unavailable'),
('Feed Mixer - Supreme 900T', 'SN2033', 3, 7, 1, '2023-11-10', 15000.00, 'fair', 'removed'),
('Feed Mixer - Supreme 900T', 'SN2034', 3, 7, 1, '2023-11-10', 15000.00, 'poor', 'available'),
('Feed Mixer - Kuhn Knight 3142', 'SN2035', 3, 8, 1, '2023-12-15', 15200.00, 'new', 'available'),
('Feed Mixer - Kuhn Knight 3142', 'SN2036', 3, 8, 1, '2023-12-15', 15200.00, 'new', 'available'),
('Feed Mixer - Kuhn Knight 3142', 'SN2037', 3, 8, 1, '2023-12-15', 15200.00, 'good', 'unavailable'),
('Feed Mixer - Kuhn Knight 3142', 'SN2038', 3, 8, 1, '2023-12-15', 15200.00, 'fair', 'removed'),
('Feed Mixer - Kuhn Knight 3142', 'SN2039', 3, 8, 1, '2023-12-15', 15200.00, 'poor', 'removed'),
-- Store 2, Sub_Category 1 to 8
('Tractor - John Deere 5100', 'SN2040', 1, 1, 2, '2023-05-10', 25000.00, 'new', 'available'),
('Tractor - John Deere 5100', 'SN2041', 1, 1, 2, '2023-05-10', 25000.00, 'new', 'available'),
('Tractor - John Deere 5100', 'SN2042', 1, 1, 2, '2023-05-10', 25000.00, 'good', 'unavailable'),
('Tractor - John Deere 5100', 'SN2043', 1, 1, 2, '2023-05-10', 25000.00, 'fair', 'removed'),
('Tractor - John Deere 5100', 'SN2044', 1, 1, 2, '2023-05-10', 25000.00, 'poor', 'available'),
('Tractor - Kubota M7060', 'SN2045', 1, 2, 2, '2023-06-15', 24000.00, 'new', 'available'),
('Tractor - Kubota M7060', 'SN2046', 1, 2, 2, '2023-06-15', 24000.00, 'new', 'available'),
('Tractor - Kubota M7060', 'SN2047', 1, 2, 2, '2023-06-15', 24000.00, 'good', 'unavailable'),
('Tractor - Kubota M7060', 'SN2048', 1, 2, 2, '2023-06-15', 24000.00, 'fair', 'removed'),
('Tractor - Kubota M7060', 'SN2049', 1, 2, 2, '2023-06-15', 24000.00, 'poor', 'available'),
('Tractor - New Holland T7', 'SN2050', 1, 3, 2, '2023-07-20', 26000.00, 'new', 'available'),
('Tractor - New Holland T7', 'SN2051', 1, 3, 2, '2023-07-20', 26000.00, 'new', 'available'),
('Tractor - New Holland T7', 'SN2052', 1, 3, 2, '2023-07-20', 26000.00, 'good', 'unavailable'),
('Tractor - New Holland T7', 'SN2053', 1, 3, 2, '2023-07-20', 26000.00, 'fair', 'removed'),
('Tractor - New Holland T7', 'SN2054', 1, 3, 2, '2023-07-20', 26000.00, 'poor', 'available'),
('Cultivator - Field King', 'SN2055', 2, 4, 2, '2023-08-25', 8000.00, 'new', 'available'),
('Cultivator - Field King', 'SN2056', 2, 4, 2, '2023-08-25', 8000.00, 'new', 'available'),
('Cultivator - Field King', 'SN2057', 2, 4, 2, '2023-08-25', 8000.00, 'good', 'unavailable'),
('Cultivator - Field King', 'SN2058', 2, 4, 2, '2023-08-25', 8000.00, 'fair', 'removed'),
('Cultivator - Field King', 'SN2059', 2, 4, 2, '2023-08-25', 8000.00, 'poor', 'available'),
('Cultivator - Great Plains Spartan II', 'SN2060', 2, 5, 2, '2023-09-30', 8200.00, 'new', 'available'),
('Cultivator - Great Plains Spartan II', 'SN2061', 2, 5, 2, '2023-09-30', 8200.00, 'new', 'available'),
('Cultivator - Great Plains Spartan II', 'SN2062', 2, 5, 2, '2023-09-30', 8200.00, 'good', 'unavailable'),
('Cultivator - Great Plains Spartan II', 'SN2063', 2, 5, 2, '2023-09-30', 8200.00, 'fair', 'removed'),
('Cultivator - Great Plains Spartan II', 'SN2064', 2, 5, 2, '2023-09-30', 8200.00, 'poor', 'available'),
('Cultivator - Land Pride APS1548', 'SN2065', 2, 6, 2, '2023-10-05', 7900.00, 'new', 'available'),
('Cultivator - Land Pride APS1548', 'SN2066', 2, 6, 2, '2023-10-05', 7900.00, 'new', 'available'),
('Cultivator - Land Pride APS1548', 'SN2067', 2, 6, 2, '2023-10-05', 7900.00, 'good', 'unavailable'),
('Cultivator - Land Pride APS1548', 'SN2068', 2, 6, 2, '2023-10-05', 7900.00, 'fair', 'removed'),
('Cultivator - Land Pride APS1548', 'SN2069', 2, 6, 2, '2023-10-05', 7900.00, 'poor', 'available'),
('Feed Mixer - Supreme 900T', 'SN2070', 3, 7, 2, '2023-11-10', 15000.00, 'new', 'available'),
('Feed Mixer - Supreme 900T', 'SN2071', 3, 7, 2, '2023-11-10', 15000.00, 'new', 'available'),
('Feed Mixer - Supreme 900T', 'SN2072', 3, 7, 2, '2023-11-10', 15000.00, 'good', 'unavailable'),
('Feed Mixer - Supreme 900T', 'SN2073', 3, 7, 2, '2023-11-10', 15000.00, 'fair', 'removed'),
('Feed Mixer - Supreme 900T', 'SN2074', 3, 7, 2, '2023-11-10', 15000.00, 'poor', 'available'),
('Feed Mixer - Kuhn Knight 3142', 'SN2075', 3, 8, 2, '2023-12-15', 15200.00, 'new', 'removed'),
('Feed Mixer - Kuhn Knight 3142', 'SN2076', 3, 8, 2, '2023-12-15', 15200.00, 'new', 'removed'),
('Feed Mixer - Kuhn Knight 3142', 'SN2077', 3, 8, 2, '2023-12-15', 15200.00, 'good', 'unavailable'),
('Feed Mixer - Kuhn Knight 3142', 'SN2078', 3, 8, 2, '2023-12-15', 15200.00, 'fair', 'removed'),
('Feed Mixer - Kuhn Knight 3142', 'SN2079', 3, 8, 2, '2023-12-15', 15200.00, 'poor', 'removed'),
-- Store 3, Sub_Category 1 to 8
('Tractor - John Deere 5100', 'SN2080', 1, 1, 3, '2023-05-10', 25000.00, 'new', 'available'),
('Tractor - John Deere 5100', 'SN2081', 1, 1, 3, '2023-05-10', 25000.00, 'new', 'available'),
('Tractor - John Deere 5100', 'SN2082', 1, 1, 3, '2023-05-10', 25000.00, 'good', 'unavailable'),
('Tractor - John Deere 5100', 'SN2083', 1, 1, 3, '2023-05-10', 25000.00, 'fair', 'removed'),
('Tractor - John Deere 5100', 'SN2084', 1, 1, 3, '2023-05-10', 25000.00, 'poor', 'available'),
('Tractor - Kubota M7060', 'SN2085', 1, 2, 3, '2023-06-15', 24000.00, 'new', 'available'),
('Tractor - Kubota M7060', 'SN2086', 1, 2, 3, '2023-06-15', 24000.00, 'new', 'available'),
('Tractor - Kubota M7060', 'SN2087', 1, 2, 3, '2023-06-15', 24000.00, 'good', 'unavailable'),
('Tractor - Kubota M7060', 'SN2088', 1, 2, 3, '2023-06-15', 24000.00, 'fair', 'removed'),
('Tractor - Kubota M7060', 'SN2089', 1, 2, 3, '2023-06-15', 24000.00, 'poor', 'available'),
('Tractor - New Holland T7', 'SN2090', 1, 3, 3, '2023-07-20', 26000.00, 'new', 'available'),
('Tractor - New Holland T7', 'SN2091', 1, 3, 3, '2023-07-20', 26000.00, 'new', 'available'),
('Tractor - New Holland T7', 'SN2092', 1, 3, 3, '2023-07-20', 26000.00, 'good', 'unavailable'),
('Tractor - New Holland T7', 'SN2093', 1, 3, 3, '2023-07-20', 26000.00, 'fair', 'removed'),
('Tractor - New Holland T7', 'SN2094', 1, 3, 3, '2023-07-20', 26000.00, 'poor', 'available'),
('Cultivator - Field King', 'SN2095', 2, 4, 3, '2023-08-25', 8000.00, 'new', 'available'),
('Cultivator - Field King', 'SN2096', 2, 4, 3, '2023-08-25', 8000.00, 'new', 'available'),
('Cultivator - Field King', 'SN2097', 2, 4, 3, '2023-08-25', 8000.00, 'good', 'unavailable'),
('Cultivator - Field King', 'SN2098', 2, 4, 3, '2023-08-25', 8000.00, 'fair', 'removed'),
('Cultivator - Field King', 'SN2099', 2, 4, 3, '2023-08-25', 8000.00, 'poor', 'available'),
('Cultivator - Great Plains Spartan II', 'SN2100', 2, 5, 3, '2023-09-30', 8200.00, 'new', 'available'),
('Cultivator - Great Plains Spartan II', 'SN2101', 2, 5, 3, '2023-09-30', 8200.00, 'new', 'available'),
('Cultivator - Great Plains Spartan II', 'SN2102', 2, 5, 3, '2023-09-30', 8200.00, 'good', 'unavailable'),
('Cultivator - Great Plains Spartan II', 'SN2103', 2, 5, 3, '2023-09-30', 8200.00, 'fair', 'removed'),
('Cultivator - Great Plains Spartan II', 'SN2104', 2, 5, 3, '2023-09-30', 8200.00, 'poor', 'available'),
('Cultivator - Land Pride APS1548', 'SN2105', 2, 6, 3, '2023-10-05', 7900.00, 'new', 'available'),
('Cultivator - Land Pride APS1548', 'SN2106', 2, 6, 3, '2023-10-05', 7900.00, 'new', 'available'),
('Cultivator - Land Pride APS1548', 'SN2107', 2, 6, 3, '2023-10-05', 7900.00, 'good', 'unavailable'),
('Cultivator - Land Pride APS1548', 'SN2108', 2, 6, 3, '2023-10-05', 7900.00, 'fair', 'removed'),
('Cultivator - Land Pride APS1548', 'SN2109', 2, 6, 3, '2023-10-05', 7900.00, 'poor', 'available'),
('Feed Mixer - Supreme 900T', 'SN2110', 3, 7, 3, '2023-11-10', 15000.00, 'new', 'available'),
('Feed Mixer - Supreme 900T', 'SN2111', 3, 7, 3, '2023-11-10', 15000.00, 'new', 'available'),
('Feed Mixer - Supreme 900T', 'SN2112', 3, 7, 3, '2023-11-10', 15000.00, 'good', 'unavailable'),
('Feed Mixer - Supreme 900T', 'SN2113', 3, 7, 3, '2023-11-10', 15000.00, 'fair', 'removed'),
('Feed Mixer - Supreme 900T', 'SN2114', 3, 7, 3, '2023-11-10', 15000.00, 'poor', 'available'),
('Feed Mixer - Kuhn Knight 3142', 'SN2115', 3, 8, 3, '2023-12-15', 15200.00, 'new', 'removed'),
('Feed Mixer - Kuhn Knight 3142', 'SN2116', 3, 8, 3, '2023-12-15', 15200.00, 'new', 'removed'),
('Feed Mixer - Kuhn Knight 3142', 'SN2117', 3, 8, 3, '2023-12-15', 15200.00, 'good', 'unavailable'),
('Feed Mixer - Kuhn Knight 3142', 'SN2118', 3, 8, 3, '2023-12-15', 15200.00, 'fair', 'removed'),
('Feed Mixer - Kuhn Knight 3142', 'SN2119', 3, 8, 3, '2023-12-15', 15200.00, 'poor', 'removed');




-- Insert data into Equipment_Stock table
INSERT INTO Equipment_Stock (store_id, sub_category_id, available_quantity) VALUES
(1, 1, 2), -- Tractor - Tractor - John Deere 5100
(2, 1, 1), -- Tractor - Tractor - John Deere 5100
(2, 2, 1), -- Tractor - Tractor - Kubota M7060
(3, 3, 1), -- Tractor - Tractor - New Holland T7
(1, 4, 1), -- Cultivator - Cultivator - Field King
(2, 5, 1), -- Cultivator - Cultivator - Great Plains Spartan II
(3, 6, 1), -- Cultivator - Cultivator - Land Pride APS1548
(1, 7, 1), -- Feed Mixer - Feed Mixer - Supreme 900T
(2, 8, 1), -- Feed Mixer - Feed Mixer - Kuhn Knight 3142
(3, 9, 1), -- Feed Mixer - Feed Mixer - Penta 8030
(1, 10, 1), -- Digger - Digger - Caterpillar 330
(2, 11, 1), -- Digger - Digger - Komatsu PC200
(3, 12, 1), -- Digger - John Deere 50G
(1, 13, 1), -- Lawn Mower - Honda HRX217VKA
(2, 14, 1), -- Lawn Mower - Toro TimeMaster
(3, 15, 1), -- Lawn Mower - Husqvarna LC221RH
(1, 16, 1), -- Sprayer - John Deere R4023
(2, 17, 1), -- Sprayer - Hardi Navigator 4000
(3, 18, 1), -- Sprayer - Amazone UX5200
(1, 19, 1), -- Chainsaw - Stihl MS 250
(2, 20, 1), -- Chainsaw - Husqvarna 455 Rancher
(3, 21, 1); -- Chainsaw - Echo CS-590

-- Re-insert existing and new Equipment_Stock data
UPDATE Equipment_Stock 
SET available_quantity = available_quantity + 5
WHERE (store_id, sub_category_id) IN 
((1, 1), (2, 2), (3, 3), (1, 4), (2, 5), (3, 6), (1, 7), (2, 8), (3, 9), 
 (1, 10), (2, 11), (3, 12), (1, 13), (2, 14), (3, 15), (1, 16), (2, 17), (3, 18), 
 (1, 19), (2, 20), (3, 21));
 
INSERT INTO Equipment_Stock (store_id, sub_category_id, available_quantity) VALUES
(1, 1, 5), 
(2, 2, 5), 
(3, 3, 5), 
(1, 4, 5), 
(2, 5, 5), 
(3, 6, 5), 
(1, 7, 5), 
(2, 8, 5), 
(3, 9, 5), 
(1, 10, 5), 
(2, 11, 5), 
(3, 12, 5), 
(1, 13, 5), 
(2, 14, 5), 
(3, 15, 5), 
(1, 16, 5), 
(2, 17, 5), 
(3, 18, 5), 
(1, 19, 5), 
(2, 20, 5), 
(3, 21, 5)
ON DUPLICATE KEY UPDATE available_quantity = available_quantity + 5;


-- Insert data into Payments table
INSERT INTO Payments (amount, payment_date, user_id) VALUES
(10000.00, '2024-05-20 08:00:00', 1),  -- Payment for booking 1
(16000.00, '2024-05-22 09:00:00', 2),  -- Payment for booking 2
(20000.00, '2024-06-18 10:00:00', 3);  -- Payment for booking 3

-- Calculate the payment amounts based on the booking data
INSERT INTO Payments (amount, payment_date, user_id) VALUES
((DATEDIFF('2024-05-25 14:00:00', '2024-05-04 11:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 4))), '2024-05-04 11:00:00', 4),
((DATEDIFF('2024-05-30 13:00:00', '2024-05-05 12:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 5))), '2024-05-05 12:00:00', 5),
((DATEDIFF('2024-06-01 12:00:00', '2024-05-06 13:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 6))), '2024-05-06 13:00:00', 6),
((DATEDIFF('2024-06-02 11:00:00', '2024-05-07 14:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 7))), '2024-05-07 14:00:00', 7),
((DATEDIFF('2024-06-03 10:00:00', '2024-05-08 15:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 8))), '2024-05-08 15:00:00', 8),
((DATEDIFF('2024-06-04 09:00:00', '2024-05-09 16:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 9))), '2024-05-09 16:00:00', 9),
((DATEDIFF('2024-06-05 08:00:00', '2024-05-10 17:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 10))), '2024-05-10 17:00:00', 10),
((DATEDIFF('2024-06-06 07:00:00', '2024-05-11 08:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 11))), '2024-05-11 08:00:00', 1),
((DATEDIFF('2024-06-07 06:00:00', '2024-05-12 09:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 12))), '2024-05-12 09:00:00', 2),
((DATEDIFF('2024-06-08 05:00:00', '2024-05-13 10:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 13))), '2024-05-13 10:00:00', 3),
((DATEDIFF('2024-06-09 04:00:00', '2024-05-14 11:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 14))), '2024-05-14 11:00:00', 4),
((DATEDIFF('2024-06-10 03:00:00', '2024-05-15 12:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 15))), '2024-05-15 12:00:00', 5),
((DATEDIFF('2024-06-11 02:00:00', '2024-05-16 13:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 16))), '2024-05-16 13:00:00', 6),
((DATEDIFF('2024-06-12 01:00:00', '2024-05-17 14:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 17))), '2024-05-17 14:00:00', 7),
((DATEDIFF('2024-06-13 00:00:00', '2024-05-18 15:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 18))), '2024-05-18 15:00:00', 8),
((DATEDIFF('2024-06-14 23:00:00', '2024-05-19 16:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 19))), '2024-05-19 16:00:00', 9),
((DATEDIFF('2024-06-15 22:00:00', '2024-05-20 17:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 20))), '2024-05-20 17:00:00', 10),
((DATEDIFF('2024-06-16 21:00:00', '2024-05-21 08:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 21))), '2024-05-21 08:00:00', 1),
((DATEDIFF('2024-06-17 20:00:00', '2024-05-22 09:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 22))), '2024-05-22 09:00:00', 2),
((DATEDIFF('2024-06-18 19:00:00', '2024-05-23 10:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 23))), '2024-05-23 10:00:00', 3),
((DATEDIFF('2024-06-19 18:00:00', '2024-05-24 11:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 24))), '2024-05-24 11:00:00', 4),
((DATEDIFF('2024-06-20 17:00:00', '2024-05-25 12:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 25))), '2024-05-25 12:00:00', 5),
((DATEDIFF('2024-06-21 16:00:00', '2024-05-26 13:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 26))), '2024-05-26 13:00:00', 6),
((DATEDIFF('2024-06-22 15:00:00', '2024-05-27 14:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 27))), '2024-05-27 14:00:00', 7),
((DATEDIFF('2024-06-23 14:00:00', '2024-05-28 15:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 28))), '2024-05-28 15:00:00', 8),
((DATEDIFF('2024-06-24 13:00:00', '2024-05-29 16:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 29))), '2024-05-29 16:00:00', 9),
((DATEDIFF('2024-06-25 12:00:00', '2024-05-30 17:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 30))), '2024-05-30 17:00:00', 10),
((DATEDIFF('2024-05-10 17:00:00', '2024-05-01 08:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 31))), '2024-05-01 08:00:00', 1),
((DATEDIFF('2024-05-15 16:00:00', '2024-05-02 09:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 32))), '2024-05-02 09:00:00', 2),
((DATEDIFF('2024-05-20 15:00:00', '2024-05-03 10:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 33))), '2024-05-03 10:00:00', 3),
((DATEDIFF('2024-05-25 14:00:00', '2024-05-04 11:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 34))), '2024-05-04 11:00:00', 4),
((DATEDIFF('2024-05-30 13:00:00', '2024-05-05 12:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 35))), '2024-05-05 12:00:00', 5),
((DATEDIFF('2024-06-01 12:00:00', '2024-05-06 13:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 36))), '2024-05-06 13:00:00', 6),
((DATEDIFF('2024-06-02 11:00:00', '2024-05-07 14:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 37))), '2024-05-07 14:00:00', 7),
((DATEDIFF('2024-06-03 10:00:00', '2024-05-08 15:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 38))), '2024-05-08 15:00:00', 8),
((DATEDIFF('2024-06-04 09:00:00', '2024-05-09 16:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 39))), '2024-05-09 16:00:00', 9),
((DATEDIFF('2024-06-05 08:00:00', '2024-05-10 17:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 40))), '2024-05-10 17:00:00', 10),
((DATEDIFF('2024-06-06 07:00:00', '2024-05-11 08:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 41))), '2024-05-11 08:00:00', 1),
((DATEDIFF('2024-06-07 06:00:00', '2024-05-12 09:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 42))), '2024-05-12 09:00:00', 2),
((DATEDIFF('2024-06-08 05:00:00', '2024-05-13 10:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 43))), '2024-05-13 10:00:00', 3),
((DATEDIFF('2024-06-09 04:00:00', '2024-05-14 11:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 44))), '2024-05-14 11:00:00', 4),
((DATEDIFF('2024-06-10 03:00:00', '2024-05-15 12:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 45))), '2024-05-15 12:00:00', 5),
((DATEDIFF('2024-06-11 02:00:00', '2024-05-16 13:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 46))), '2024-05-16 13:00:00', 6),
((DATEDIFF('2024-06-12 01:00:00', '2024-05-17 14:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 47))), '2024-05-17 14:00:00', 7),
((DATEDIFF('2024-06-13 00:00:00', '2024-05-18 15:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 48))), '2024-05-18 15:00:00', 8),
((DATEDIFF('2024-06-14 23:00:00', '2024-05-19 16:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 49))), '2024-05-19 16:00:00', 9),
((DATEDIFF('2024-06-15 22:00:00', '2024-05-20 17:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 50))), '2024-05-20 17:00:00', 10),
((DATEDIFF('2024-06-16 21:00:00', '2024-05-21 08:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 51))), '2024-05-21 08:00:00', 1),
((DATEDIFF('2024-06-17 20:00:00', '2024-05-22 09:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 52))), '2024-05-22 09:00:00', 2),
((DATEDIFF('2024-06-18 19:00:00', '2024-05-23 10:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 53))), '2024-05-23 10:00:00', 3),
((DATEDIFF('2024-06-19 18:00:00', '2024-05-24 11:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 54))), '2024-05-24 11:00:00', 4),
((DATEDIFF('2024-06-20 17:00:00', '2024-05-25 12:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 55))), '2024-05-25 12:00:00', 5),
((DATEDIFF('2024-06-21 16:00:00', '2024-05-26 13:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 56))), '2024-05-26 13:00:00', 6),
((DATEDIFF('2024-06-22 15:00:00', '2024-05-27 14:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 57))), '2024-05-27 14:00:00', 7),
((DATEDIFF('2024-06-23 14:00:00', '2024-05-28 15:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 58))), '2024-05-28 15:00:00', 8),
((DATEDIFF('2024-06-24 13:00:00', '2024-05-29 16:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 59))), '2024-05-29 16:00:00', 9),
((DATEDIFF('2024-06-25 12:00:00', '2024-05-30 17:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 60))), '2024-05-30 17:00:00', 10);

INSERT INTO Bookings (user_id, equipment_id, checkout_datetime, return_datetime, status, line_total) VALUES
(4, 4, '2024-05-04 11:00:00', '2024-05-25 14:00:00', 'pending', (DATEDIFF('2024-05-25 14:00:00', '2024-05-04 11:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 4)))),
(5, 5, '2024-05-05 12:00:00', '2024-05-30 13:00:00', 'checked_out', (DATEDIFF('2024-05-30 13:00:00', '2024-05-05 12:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 5)))),
(6, 6, '2024-05-06 13:00:00', '2024-06-01 12:00:00', 'returned', (DATEDIFF('2024-06-01 12:00:00', '2024-05-06 13:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 6)))),
(7, 7, '2024-05-07 14:00:00', '2024-06-02 11:00:00', 'cancelled', (DATEDIFF('2024-06-02 11:00:00', '2024-05-07 14:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 7)))),
(8, 8, '2024-05-08 15:00:00', '2024-06-03 10:00:00', 'booked', (DATEDIFF('2024-06-03 10:00:00', '2024-05-08 15:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 8)))),
(9, 9, '2024-05-09 16:00:00', '2024-06-04 09:00:00', 'pending', (DATEDIFF('2024-06-04 09:00:00', '2024-05-09 16:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 9)))),
(10, 10, '2024-05-10 17:00:00', '2024-06-05 08:00:00', 'checked_out', (DATEDIFF('2024-06-05 08:00:00', '2024-05-10 17:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 10)))),
(1, 11, '2024-05-11 08:00:00', '2024-06-06 07:00:00', 'returned', (DATEDIFF('2024-06-06 07:00:00', '2024-05-11 08:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 11)))),
(2, 12, '2024-05-12 09:00:00', '2024-06-07 06:00:00', 'cancelled', (DATEDIFF('2024-06-07 06:00:00', '2024-05-12 09:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 12)))),
(3, 13, '2024-05-13 10:00:00', '2024-06-08 05:00:00', 'booked', (DATEDIFF('2024-06-08 05:00:00', '2024-05-13 10:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 13)))),
(4, 14, '2024-05-14 11:00:00', '2024-06-09 04:00:00', 'pending', (DATEDIFF('2024-06-09 04:00:00', '2024-05-14 11:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 14)))),
(5, 15, '2024-05-15 12:00:00', '2024-06-10 03:00:00', 'checked_out', (DATEDIFF('2024-06-10 03:00:00', '2024-05-15 12:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 15)))),
(6, 16, '2024-05-16 13:00:00', '2024-06-11 02:00:00', 'returned', (DATEDIFF('2024-06-11 02:00:00', '2024-05-16 13:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 16)))),
(7, 17, '2024-05-17 14:00:00', '2024-06-12 01:00:00', 'cancelled', (DATEDIFF('2024-06-12 01:00:00', '2024-05-17 14:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 17)))),
(8, 18, '2024-05-18 15:00:00', '2024-06-13 00:00:00', 'booked', (DATEDIFF('2024-06-13 00:00:00', '2024-05-18 15:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 18)))),
(9, 19, '2024-05-19 16:00:00', '2024-06-14 23:00:00', 'pending', (DATEDIFF('2024-06-14 23:00:00', '2024-05-19 16:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 19)))),
(10, 20, '2024-05-20 17:00:00', '2024-06-15 22:00:00', 'checked_out', (DATEDIFF('2024-06-15 22:00:00', '2024-05-20 17:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 20)))),
(1, 21, '2024-05-21 08:00:00', '2024-06-16 21:00:00', 'returned', (DATEDIFF('2024-06-16 21:00:00', '2024-05-21 08:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 21)))),
(2, 22, '2024-05-22 09:00:00', '2024-06-17 20:00:00', 'cancelled', (DATEDIFF('2024-06-17 20:00:00', '2024-05-22 09:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 22)))),
(3, 23, '2024-05-23 10:00:00', '2024-06-18 19:00:00', 'booked', (DATEDIFF('2024-06-18 19:00:00', '2024-05-23 10:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 23)))),
(4, 24, '2024-05-24 11:00:00', '2024-06-19 18:00:00', 'pending', (DATEDIFF('2024-06-19 18:00:00', '2024-05-24 11:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 24)))),
(5, 25, '2024-05-25 12:00:00', '2024-06-20 17:00:00', 'checked_out', (DATEDIFF('2024-06-20 17:00:00', '2024-05-25 12:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 25)))),
(6, 26, '2024-05-26 13:00:00', '2024-06-21 16:00:00', 'returned', (DATEDIFF('2024-06-21 16:00:00', '2024-05-26 13:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 26)))),
(7, 27, '2024-05-27 14:00:00', '2024-06-22 15:00:00', 'cancelled', (DATEDIFF('2024-06-22 15:00:00', '2024-05-27 14:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 27)))),
(8, 28, '2024-05-28 15:00:00', '2024-06-23 14:00:00', 'booked', (DATEDIFF('2024-06-23 14:00:00', '2024-05-28 15:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 28)))),
(9, 29, '2024-05-29 16:00:00', '2024-06-24 13:00:00', 'pending', (DATEDIFF('2024-06-24 13:00:00', '2024-05-29 16:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 29)))),
(10, 30, '2024-05-30 17:00:00', '2024-06-25 12:00:00', 'checked_out', (DATEDIFF('2024-06-25 12:00:00', '2024-05-30 17:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 30)))),
(1, 31, '2024-05-01 08:00:00', '2024-05-10 17:00:00', 'booked', (DATEDIFF('2024-05-10 17:00:00', '2024-05-01 08:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 31)))),
(2, 32, '2024-05-02 09:00:00', '2024-05-15 16:00:00', 'booked', (DATEDIFF('2024-05-15 16:00:00', '2024-05-02 09:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 32)))),
(3, 33, '2024-05-03 10:00:00', '2024-05-20 15:00:00', 'booked', (DATEDIFF('2024-05-20 15:00:00', '2024-05-03 10:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 33)))),
(4, 34, '2024-05-04 11:00:00', '2024-05-25 14:00:00', 'pending', (DATEDIFF('2024-05-25 14:00:00', '2024-05-04 11:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 34)))),
(5, 35, '2024-05-05 12:00:00', '2024-05-30 13:00:00', 'checked_out', (DATEDIFF('2024-05-30 13:00:00', '2024-05-05 12:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 35)))),
(6, 36, '2024-05-06 13:00:00', '2024-06-01 12:00:00', 'returned', (DATEDIFF('2024-06-01 12:00:00', '2024-05-06 13:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 36)))),
(7, 37, '2024-05-07 14:00:00', '2024-06-02 11:00:00', 'cancelled', (DATEDIFF('2024-06-02 11:00:00', '2024-05-07 14:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 37)))),
(8, 38, '2024-05-08 15:00:00', '2024-06-03 10:00:00', 'booked', (DATEDIFF('2024-06-03 10:00:00', '2024-05-08 15:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 38)))),
(9, 39, '2024-05-09 16:00:00', '2024-06-04 09:00:00', 'pending', (DATEDIFF('2024-06-04 09:00:00', '2024-05-09 16:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 39)))),
(10, 40, '2024-05-10 17:00:00', '2024-06-05 08:00:00', 'checked_out', (DATEDIFF('2024-06-05 08:00:00', '2024-05-10 17:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 40)))),
(1, 41, '2024-05-11 08:00:00', '2024-06-06 07:00:00', 'returned', (DATEDIFF('2024-06-06 07:00:00', '2024-05-11 08:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 41)))),
(2, 42, '2024-05-12 09:00:00', '2024-06-07 06:00:00', 'cancelled', (DATEDIFF('2024-06-07 06:00:00', '2024-05-12 09:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 42)))),
(3, 43, '2024-05-13 10:00:00', '2024-06-08 05:00:00', 'booked', (DATEDIFF('2024-06-08 05:00:00', '2024-05-13 10:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 43)))),
(4, 44, '2024-05-14 11:00:00', '2024-06-09 04:00:00', 'pending', (DATEDIFF('2024-06-09 04:00:00', '2024-05-14 11:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 44)))),
(5, 45, '2024-05-15 12:00:00', '2024-06-10 03:00:00', 'checked_out', (DATEDIFF('2024-06-10 03:00:00', '2024-05-15 12:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 45)))),
(6, 46, '2024-05-16 13:00:00', '2024-06-11 02:00:00', 'returned', (DATEDIFF('2024-06-11 02:00:00', '2024-05-16 13:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 46)))),
(7, 47, '2024-05-17 14:00:00', '2024-06-12 01:00:00', 'cancelled', (DATEDIFF('2024-06-12 01:00:00', '2024-05-17 14:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 47)))),
(8, 48, '2024-05-18 15:00:00', '2024-06-13 00:00:00', 'booked', (DATEDIFF('2024-06-13 00:00:00', '2024-05-18 15:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 48)))),
(9, 49, '2024-05-19 16:00:00', '2024-06-14 23:00:00', 'pending', (DATEDIFF('2024-06-14 23:00:00', '2024-05-19 16:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 49)))),
(10, 50, '2024-05-20 17:00:00', '2024-06-15 22:00:00', 'checked_out', (DATEDIFF('2024-06-15 22:00:00', '2024-05-20 17:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 50)))),
(1, 51, '2024-05-21 08:00:00', '2024-06-16 21:00:00', 'returned', (DATEDIFF('2024-06-16 21:00:00', '2024-05-21 08:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 51)))),
(2, 52, '2024-05-22 09:00:00', '2024-06-17 20:00:00', 'cancelled', (DATEDIFF('2024-06-17 20:00:00', '2024-05-22 09:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 52)))),
(3, 53, '2024-05-23 10:00:00', '2024-06-18 19:00:00', 'booked', (DATEDIFF('2024-06-18 19:00:00', '2024-05-23 10:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 53)))),
(4, 54, '2024-05-24 11:00:00', '2024-06-19 18:00:00', 'pending', (DATEDIFF('2024-06-19 18:00:00', '2024-05-24 11:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 54)))),
(5, 55, '2024-05-25 12:00:00', '2024-06-20 17:00:00', 'checked_out', (DATEDIFF('2024-06-20 17:00:00', '2024-05-25 12:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 55)))),
(6, 56, '2024-05-26 13:00:00', '2024-06-21 16:00:00', 'returned', (DATEDIFF('2024-06-21 16:00:00', '2024-05-26 13:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 56)))),
(7, 57, '2024-05-27 14:00:00', '2024-06-22 15:00:00', 'cancelled', (DATEDIFF('2024-06-22 15:00:00', '2024-05-27 14:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 57)))),
(8, 58, '2024-05-28 15:00:00', '2024-06-23 14:00:00', 'booked', (DATEDIFF('2024-06-23 14:00:00', '2024-05-28 15:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 58)))),
(9, 59, '2024-05-29 16:00:00', '2024-06-24 13:00:00', 'pending', (DATEDIFF('2024-06-24 13:00:00', '2024-05-29 16:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 59)))),
(10, 60, '2024-05-30 17:00:00', '2024-06-25 12:00:00', 'checked_out', (DATEDIFF('2024-06-25 12:00:00', '2024-05-30 17:00:00') * (SELECT hire_cost FROM Sub_Category WHERE sub_category_id = (SELECT sub_category_id FROM Equipment WHERE equipment_id = 60))));




-- Insert data into Orders table
-- Assumption: customer_id matches user_id for simplicity
INSERT INTO Orders (shipping_address, special_instruction, payment_method, customer_id, payment_id, status) VALUES
('123 Home St, Cityville', 'Please handle with care.', 'Credit Card', 1, 1, 'Confirmed'),
('456 Work Ave, Townsville', 'Leave at the front door.', 'Credit Card', 2, 2, 'Confirmed'),
('789 Other Rd, Villageville', 'Call on arrival.', 'Credit Card', 3, 3, 'Confirmed'),
('123 New St, Hamlet', 'Ring the bell.', 'Credit Card', 4, 4, 'Confirmed'),
('456 Old St, Metropolis', 'Use side entrance.', 'Credit Card', 5, 5, 'Confirmed'),
('789 Main St, City', 'Do not leave at door.', 'Credit Card', 6, 6, 'Confirmed'),
('321 Oak St, Woodsville', 'Contact on delivery.', 'Credit Card', 7, 7, 'Confirmed'),
('654 Pine St, Forestville', 'Deliver to neighbor.', 'Credit Card', 8, 8, 'Confirmed'),
('987 Cedar St, Hilltown', 'Use back entrance.', 'Credit Card', 9, 9, 'Confirmed'),
('135 Birch St, Rivertown', 'Handle with care.', 'Credit Card', 10, 10, 'Confirmed');

-- Insert data into OrderBookings table
-- Mapping each order to corresponding booking id
INSERT INTO OrderBookings (order_id, booking_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10),
(1, 11),
(1, 12),
(1, 13),
(4, 14),
(5, 15),
(6, 16),
(7, 17),
(8, 18),
(9, 19),
(2, 20),
(1, 21),
(2, 22),
(3, 23),
(4, 24),
(5, 25),
(6, 26),
(7, 27),
(8, 28),
(9, 29),
(3, 30),
(1, 31),
(2, 32),
(3, 33),
(4, 34),
(5, 35),
(6, 36),
(7, 37),
(8, 38),
(9, 39),
(2, 40),
(1, 41),
(2, 42),
(3, 43),
(4, 44),
(5, 45),
(6, 46),
(7, 47),
(8, 48),
(9, 49),
(5, 50),
(1, 51),
(2, 52),
(3, 53),
(4, 54),
(5, 55),
(6, 56),
(7, 57);




-- Inserting Data into Cart Table
INSERT INTO Cart (user_id, equipment_id, checkout_datetime, return_datetime, quantity, total_cost) VALUES
(1, 1, '2024-06-01 10:00:00', '2024-06-05 10:00:00', 1, 19200),  
(2, 2, '2024-06-02 09:00:00', '2024-06-07 09:00:00', 1, 22800),  
(3, 3, '2024-06-03 08:00:00', '2024-06-08 08:00:00', 1, 25200),  
(1, 4, '2024-06-04 11:00:00', '2024-06-09 11:00:00', 1, 9600),  
(2, 5, '2024-06-05 12:00:00', '2024-06-10 12:00:00', 1, 10200); 

-- Insert data into Reviews table
INSERT INTO Reviews (booking_id, user_id, rating, comment) VALUES
(1, 1, 5, 'Excellent service and equipment. Highly recommend!'),
(2, 2, 4, 'Good experience, but the equipment was a bit old.'),
(3, 3, 3, 'Decent service, but the checkout process was slow.');


-- Insert data into News table
INSERT INTO News (title, content, posted_date, image_id, author_id) VALUES
('Grand Opening of New Store', 'We are excited to announce the opening of our new store in Hobsonville this May!', '2024-05-01 10:00:00', 30, 1),
('Annual Sale Event', 'Join us for our annual sale event with up to 50% off on selected equipment. Starts June 1st!', '2024-06-01 09:00:00', 31, 2),
('New Partnership', 'We are proud to announce our new partnership with Eco Solutions to bring more sustainable products to our stores.', '2024-07-15 08:00:00', 32, 3),
('New Product Launch', 'We’re thrilled to introduce our latest range of high-tech gardening tools, available at all branches from August 10th!', '2024-08-10 12:00:00', 33, 4),
('Winter Preparation Workshop', 'Prepare your garden for winter with our free workshop on winter gardening techniques, happening September 20th.', '2024-09-20 11:00:00', 34, 5);


-- Insert data into Notifications table
INSERT INTO Notifications (user_id, message, created_at) VALUES
(19, 'Your recent booking has been confirmed. Thank you for choosing AgriHire!', '2024-05-06 08:00:00'),
(20, 'Reminder: Your equipment rental period ends tomorrow. Please prepare for return.', '2024-05-07 09:00:00'),
(21, 'Special Promotion: Enjoy 20% off on your next rental with us. Valid until the end of May!', '2024-05-08 10:00:00');



-- Insert data into Messages table
INSERT INTO Messages (sender_id, receiver_id, store_id, subject, message_text, sent_time, read_time, status) VALUES
(1, 11,1, 'Inquiry about product availability', 'Hello, I would like to know if it is possible to transfer a lawn mower from another store to my location. Thank you.', '2024-05-06 09:00:00', '2024-05-06 10:00:00', 'read'),
(11, 1,1, 'Re: Inquiry about product availability', 'Hi! Yes, we can arrange the transfer for you. It will take approximately 3 days. We will keep you updated.', '2024-05-06 10:15:00', '2024-05-06 11:00:00', 'responded'),
(2, 11,2, 'Request for equipment transfer', 'Can I request a chainsaw to be transferred to my nearest store? I need it by next week.', '2024-05-07 11:00:00', '2024-05-07 12:00:00', 'read'),
(11, 2,2, 'Re: Request for equipment transfer', 'Hello, we have checked the availability and can confirm the transfer. Expect it by this Friday.', '2024-05-07 12:30:00', '2024-05-07 13:00:00', 'responded'),
(3, 11,3, 'Equipment availability', 'Is it possible to get a feed mixer from another branch? Our project starts soon.', '2024-05-08 14:00:00', '2024-05-08 15:00:00', 'read'),
(11, 3,3, 'Re: Equipment availability', 'Certainly, we can do that. The feed mixer will be ready for pickup at your store in two days.', '2024-05-08 15:30:00', '2024-05-08 16:00:00', 'responded');





-- Insert Services data
INSERT INTO Services (equipment_id, service_date, description, cost) VALUES
(1, '2024-05-01', 'Routine maintenance', 100.00),
(2, '2024-05-02', 'Minor repairs', 200.00),
(3, '2024-05-03', 'Major overhaul', 300.00),
(4, '2024-05-04', 'Software update', 400.00),
(5, '2024-05-05', 'General checkup', 500.00),
(6, '2024-05-06', 'Routine maintenance', 100.00),
(7, '2024-05-07', 'Minor repairs', 200.00),
(8, '2024-05-08', 'Major overhaul', 300.00),
(9, '2024-05-09', 'Software update', 400.00),
(10, '2024-05-10', 'General checkup', 500.00),
(11, '2024-05-11', 'Routine maintenance', 100.00),
(12, '2024-05-12', 'Minor repairs', 200.00),
(13, '2024-05-13', 'Major overhaul', 300.00),
(14, '2024-05-14', 'Software update', 400.00),
(15, '2024-05-15', 'General checkup', 500.00),
(16, '2024-05-16', 'Routine maintenance', 100.00),
(17, '2024-05-17', 'Minor repairs', 200.00),
(18, '2024-05-18', 'Major overhaul', 300.00),
(19, '2024-05-19', 'Software update', 400.00),
(20, '2024-05-20', 'General checkup', 500.00),
(21, '2024-05-21', 'Routine maintenance', 100.00),
(22, '2024-05-22', 'Minor repairs', 200.00),
(23, '2024-05-23', 'Major overhaul', 300.00),
(24, '2024-05-24', 'Software update', 400.00),
(25, '2024-05-25', 'General checkup', 500.00),
(26, '2024-05-26', 'Routine maintenance', 100.00),
(27, '2024-05-27', 'Minor repairs', 200.00),
(28, '2024-05-28', 'Major overhaul', 300.00),
(29, '2024-05-29', 'Software update', 400.00),
(30, '2024-05-30', 'General checkup', 500.00),
(31, '2024-05-31', 'Routine maintenance', 100.00),
(32, '2024-06-01', 'Minor repairs', 200.00),
(33, '2024-06-02', 'Major overhaul', 300.00),
(34, '2024-06-03', 'Software update', 400.00),
(35, '2024-06-04', 'General checkup', 500.00),
(36, '2024-06-05', 'Routine maintenance', 100.00),
(37, '2024-06-06', 'Minor repairs', 200.00),
(38, '2024-06-07', 'Major overhaul', 300.00),
(39, '2024-06-08', 'Software update', 400.00),
(40, '2024-06-09', 'General checkup', 500.00),
(41, '2024-06-10', 'Routine maintenance', 100.00),
(42, '2024-06-11', 'Minor repairs', 200.00),
(43, '2024-06-12', 'Major overhaul', 300.00),
(44, '2024-06-13', 'Software update', 400.00),
(45, '2024-06-14', 'General checkup', 500.00),
(46, '2024-06-15', 'Routine maintenance', 100.00),
(47, '2024-06-16', 'Minor repairs', 200.00),
(48, '2024-06-17', 'Major overhaul', 300.00),
(49, '2024-06-18', 'Software update', 400.00),
(50, '2024-06-19', 'General checkup', 500.00),
(51, '2024-06-20', 'Routine maintenance', 100.00),
(52, '2024-06-21', 'Minor repairs', 200.00),
(53, '2024-06-22', 'Major overhaul', 300.00),
(54, '2024-06-23', 'Software update', 400.00),
(55, '2024-06-24', 'General checkup', 500.00),
(56, '2024-06-25', 'Routine maintenance', 100.00),
(57, '2024-06-26', 'Minor repairs', 200.00),
(58, '2024-06-27', 'Major overhaul', 300.00),
(59, '2024-06-28', 'Software update', 400.00),
(60, '2024-06-29', 'General checkup', 500.00);

-- Insert Reviews data
INSERT INTO Reviews (booking_id, user_id, rating, comment) VALUES
(1, 1, 5, 'Excellent service and equipment. Highly recommend!'),
(2, 2, 4, 'Good experience, but the equipment was a bit old.'),
(3, 3, 3, 'Decent service, but the checkout process was slow.'),
(4, 4, 4, 'Great equipment, but the rental price was high.'),
(5, 5, 2, 'The equipment was not in the best condition.');



-- Insert data into the Promotions table
INSERT INTO Promotions (title, sub_category_id, image_id, description, start_date, end_date, discount_rate) VALUES
('Spring Special on Tractors', 1, 35, 'Get 10% off on all our tractors this spring. Offer lasts till the end of June!', '2024-03-01', '2024-06-30', 10.00),
('Cultivation Machinery Discount', 4, 36, 'Special 15% discount on cultivation machinery available through June.', '2024-06-01', '2024-06-30', 15.00),
('Lawn Mower Weekend Sale', 7, 37, 'This weekend only! Save 20% on any lawn mower purchase or rental.', '2024-06-10', '2024-06-16', 20.00),
('Spring Special on Tractors', 2, 35, 'Get 10% off on all our tractors this spring. Offer lasts till the end of June!', '2024-03-01', '2024-06-30', 10.00),
('Cultivation Machinery Discount', 5, 36, 'Special 15% discount on cultivation machinery available through June.', '2024-06-01', '2024-06-30', 15.00),
('Spring Special on Tractors', 3, 35, 'Get 10% off on all our tractors this spring. Offer lasts till the end of June!', '2024-03-01', '2024-06-30', 10.00);

INSERT INTO Notifications (user_id, message) VALUES
(1, 'Your order has been shipped.'),
(2, 'Your payment has been received.'),
(1, 'Your scheduled maintenance is due next week.');

INSERT INTO Notifications (message) VALUES
('A new product has been added to your favorite category.'),
('Promotion starts tomorrow! Don\'t miss out.'),
('Your subscription has been renewed successfully.');

INSERT INTO PaymentMethods (user_id, card_type, name_on_card, expiration_month, expiration_year, digits, security_code) VALUES
(1, 'Visa', 'Ray L', '12', '25', '1234567890123456', '100'),
(1, 'MasterCard', 'Ray L', '12', '25', '1234567890123456', '100'),
(2, 'Visa', 'Zac S', '11', '24', '2345678901234567', '101'),
(2, 'MasterCard', 'Zac S', '11', '24', '2345678901234567', '101'),
(3, 'American Express', 'Rara R', '10', '23', '3456789012345678', '102'),
(4, 'Visa', 'Angela B', '09', '22', '4567890123456789', '103'),
(5, 'Visa', 'Lina W', '08', '21', '5678901234567890', '104'),
(6, 'MasterCard', 'Lulu T', '07', '20', '6789012345678901', '105'),
(7, 'Visa', 'Coco A', '06', '19', '7890123456789012', '106'),
(8, 'MasterCard', 'Cici M', '05', '18', '8901234567890123', '107'),
(9, 'American Express', 'Fafa G', '04', '17', '9012345678901234', '108'),
(10, 'Visa', 'Haha H', '03', '16', '0123456789012345', '109');








