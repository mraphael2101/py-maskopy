import mysql.connector

def print_table(title, headers, rows):
    print(f"\n{title}:")
    # Calculate column widths
    widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val)))
    
    # Print separator
    sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    print(sep)
    
    # Print headers
    header_row = "|" + "|".join(f" {str(h).ljust(widths[i])} " for i, h in enumerate(headers)) + "|"
    print(header_row)
    print(sep)
    
    # Print rows
    for row in rows:
        formatted_row = "|" + "|".join(f" {str(val).ljust(widths[i])} " for i, val in enumerate(row)) + "|"
        print(formatted_row)
    print(sep)

def run_reset():
    config = {
        'host': '127.0.0.1',
        'port': 3307,
        'user': 'root',
        'password': 'rootpwd',
        'database': 'dummy_db'
    }
    
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # Disable foreign key checks for clean truncation/deletion
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        
        # Clear existing data
        print("Clearing data...")
        cursor.execute("TRUNCATE TABLE payments;")
        cursor.execute("TRUNCATE TABLE customers;")
        
        # Re-insert original data
        print("Restoring original data...")
        
        customers_data = [
            (1, 'John Doe', 'john.doe@example.com', '555-0101'),
            (2, 'Jane Smith', 'jane.smith@testmail.org', '555-0202'),
            (3, 'Alice Brown', 'alice.b@random.net', '555-0303'),
            (4, 'Bob White', 'bob.white@dummy.com', '555-0404')
        ]
        
        print_table("Restoring Customers", ["id", "name", "email", "phone"], customers_data)
        for c_id, name, email, phone in customers_data:
            cursor.execute(
                "INSERT INTO customers (id, name, email, phone) VALUES (%s, %s, %s, %s)",
                (c_id, name, email, phone)
            )
        
        payments_data = [
            (1, 1, '1234-5678-9012-3456', 100.50),
            (2, 2, '9876-5432-1098-7654', 250.00),
            (3, 3, '1111-2222-3333-4444', 15.75),
            (4, 4, '5555-6666-7777-8888', 89.99)
        ]
        
        # We only print id, customer_id, and card_number to keep it consistent with mask_data.py table
        payment_display_data = [(p[0], p[1], p[2]) for p in payments_data]
        print_table("Restoring Payments", ["id", "customer_id", "card_number"], payment_display_data)
        for p_id, c_id, card, amount in payments_data:
            cursor.execute(
                "INSERT INTO payments (id, customer_id, card_number, amount) VALUES (%s, %s, %s, %s)",
                (p_id, c_id, card, amount)
            )
        
        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        
        conn.commit()
        print("\nDatabase reset complete.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    run_reset()
