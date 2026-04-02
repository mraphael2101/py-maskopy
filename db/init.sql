ALTER SESSION SET CONTAINER = FREEPDB1;
ALTER SESSION SET CURRENT_SCHEMA = MASKOPY;

BEGIN
  EXECUTE IMMEDIATE 'DROP TABLE payments CASCADE CONSTRAINTS';
EXCEPTION
  WHEN OTHERS THEN
    IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

BEGIN
  EXECUTE IMMEDIATE 'DROP TABLE customers CASCADE CONSTRAINTS';
EXCEPTION
  WHEN OTHERS THEN
    IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

CREATE TABLE customers (
  id NUMBER PRIMARY KEY,
  name VARCHAR2(100),
  email VARCHAR2(100),
  phone VARCHAR2(20)
);

CREATE TABLE payments (
  id NUMBER PRIMARY KEY,
  customer_id NUMBER,
  card_number VARCHAR2(19),
  amount NUMBER(10, 2),
  CONSTRAINT fk_payments_customer
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Initial data for customers
INSERT INTO customers (id, name, email, phone) VALUES (1, 'John Doe', 'john.doe@example.com', '555-0101');
INSERT INTO customers (id, name, email, phone) VALUES (2, 'Jane Smith', 'jane.smith@testmail.org', '555-0202');
INSERT INTO customers (id, name, email, phone) VALUES (3, 'Alice Brown', 'alice.b@random.net', '555-0303');
INSERT INTO customers (id, name, email, phone) VALUES (4, 'Bob White', 'bob.white@dummy.com', '555-0404');

-- Initial data for payments
INSERT INTO payments (id, customer_id, card_number, amount) VALUES (1, 1, '1234-5678-9012-3456', 100.50);
INSERT INTO payments (id, customer_id, card_number, amount) VALUES (2, 2, '9876-5432-1098-7654', 250.00);
INSERT INTO payments (id, customer_id, card_number, amount) VALUES (3, 3, '1111-2222-3333-4444', 15.75);
INSERT INTO payments (id, customer_id, card_number, amount) VALUES (4, 4, '5555-6666-7777-8888', 89.99);

COMMIT;
