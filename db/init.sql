CREATE DATABASE IF NOT EXISTS dummy_db;
USE dummy_db;

CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    card_number VARCHAR(19),
    amount DECIMAL(10, 2),
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

INSERT INTO customers (name, email, phone) VALUES
('John Doe', 'john.doe@example.com', '555-0101'),
('Jane Smith', 'jane.smith@testmail.org', '555-0202'),
('Alice Brown', 'alice.b@random.net', '555-0303'),
('Bob White', 'bob.white@dummy.com', '555-0404');

INSERT INTO payments (customer_id, card_number, amount) VALUES
(1, '1234-5678-9012-3456', 100.50),
(2, '9876-5432-1098-7654', 250.00),
(3, '1111-2222-3333-4444', 15.75),
(4, '5555-6666-7777-8888', 89.99);
