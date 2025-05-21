CREATE DATABASE IF NOT EXISTS grocs;
USE grocs;

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    image VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    phone VARCHAR(20) NOT NULL,
    delivery_option VARCHAR(20) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Users (2 admins, 4 regular)
INSERT INTO users (username, email, password, is_admin) VALUES
('admin1', 'admin1@grocs.com', '$2b$12$9X8Z3z4Y5a6b7c8d9e0f1g2h3i4j5k6l7m8n9o0p1q2r3s4t5u6v7', TRUE),
('admin2', 'admin2@grocs.com', '$2b$12$a9b8c7d6e5f4g3h2i1j0k9l8m7n6o5p4q3r2s1t0u9v8w7x6y5z4', TRUE),
('user1', 'user1@grocs.com', '$2b$12$b0c1d2e3f4g5h6i7j8k9l0m1n2o3p4q5r6s7t8u9v0w1x2y3z4', FALSE),
('user2', 'user2@grocs.com', '$2b$12$c1d2e3f4g5h6i7j8k9l0m1n2o3p4q5r6s7t8u9v0w1x2y3z4a5', FALSE),
('user3', 'user3@grocs.com', '$2b$12$d2e3f4g5h6i7j8k9l0m1n2o3p4q5r6s7t8u9v0w1x2y3z4a5b6', FALSE),
('user4', 'user4@grocs.com', '$2b$12$e3f4g5h6i7j8k9l0m1n2o3p4q5r6s7t8u9v0w1x2y3z4a5b6c7', FALSE);

-- Products (15 items, 6 categories)
INSERT INTO products (name, price, description, category, image) VALUES
('Orange', 4.50, 'Fresh and juicy oranges, perfect for a healthy snack or to add a burst of citrus to your meals.', 'Fruits', 'orange.jpg'),
('Apple', 5.00, 'Crisp and juicy apples, perfect for snacking.', 'Fruits', 'apple.jpg'),
('Avocado', 6.00, 'Creamy avocados, great for salads or guacamole.', 'Fruits', 'avocado.jpg'),
('Onion', 2.50, 'Crisp and flavorful onions, ideal for cooking or salads.', 'Vegetables', 'onion.jpg'),
('Carrot', 2.50, 'Crunchy and sweet carrots, great for salads or cooking.', 'Vegetables', 'carrot.jpg'),
('Cabbage', 3.00, 'Fresh green cabbage, perfect for coleslaw or stir-fries.', 'Vegetables', 'cabbage.jpg'),
('Milk', 3.00, 'Fresh full-cream milk, sourced from local dairies.', 'Dairy', 'milk.jpg'),
('Yogurt', 4.00, 'Creamy natural yogurt, perfect for breakfast or snacks.', 'Dairy', 'yogurt.jpg'),
('Bread', 4.00, 'Freshly baked white loaf, soft and delicious.', 'Bakery', 'bread.jpg'),
('Pastry', 5.50, 'Flaky pastries, freshly baked daily.', 'Bakery', 'pastry.jpg'),
('Beef Rump Steak', 20.00, 'High-quality beef rump steak, perfect for grilling.', 'Meat', 'beef.jpg'),
('Chicken Breast', 10.00, 'Fresh chicken breast, ideal for healthy meals.', 'Meat', 'chicken.jpg'),
('Ginger', 12.00, 'Fresh ginger root, perfect for cooking or teas.', 'Spices', 'ginger.jpg'),
('Turmeric', 10.00, 'Fresh turmeric root, great for curries or health drinks.', 'Spices', 'turmeric.jpg'),
('Cinnamon', 8.00, 'Ground cinnamon, perfect for baking or beverages.', 'Spices', 'cinnamon.jpg');

-- Orders (3 orders, different users, unique delivery options)
INSERT INTO orders (user_id, full_name, address, phone, delivery_option, total) VALUES
(3, 'User One', '123 Main St, Brisbane', '+61412345678', 'standard', 14.00),
(4, 'User Two', '456 Queen St, Brisbane', '+61487654321', 'express', 17.50),
(5, 'User Three', '789 George St, Brisbane', '+61411223344', 'green', 7.00);

-- Order Items
INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
(1, 1, 1, 4.50), -- Order 1: Orange
(1, 4, 1, 2.50), -- Order 1: Onion
(2, 2, 1, 5.00), -- Order 2: Apple
(2, 11, 1, 20.00), -- Order 2: Beef
(3, 7, 1, 3.00), -- Order 3: Milk
(3, 9, 1, 4.00); -- Order 3: Bread