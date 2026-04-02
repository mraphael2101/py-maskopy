import mysql.connector
import csv
from pathlib import Path

def print_table(title, headers, rows):
    print(f"\n{title}:")
    widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val)))
    
    sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    print(sep)
    
    header_row = "|" + "|".join(f" {str(h).ljust(widths[i])} " for i, h in enumerate(headers)) + "|"
    print(header_row)
    print(sep)
    
    for row in rows:
        formatted_row = "|" + "|".join(f" {str(val).ljust(widths[i])} " for i, val in enumerate(row)) + "|"
        print(formatted_row)
    print(sep)

def load_csv(filename):
    data = []

    abs_filename = Path(__file__).resolve().parents[1] / filename
    if not abs_filename.exists():
        print(f"Error: {abs_filename} not found.")
        return data
        
    with open(abs_filename, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

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
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        
        print("Clearing data...")
        cursor.execute("TRUNCATE TABLE payments;")
        cursor.execute("TRUNCATE TABLE customers;")
        
        print("Restoring original data from CSV...")
        
        customers_data = load_csv('db/data/customers.csv')
        if customers_data:
            display_rows = [[c['id'], c['name'], c['email'], c['phone']] for c in customers_data]
            print_table("Restoring Customers", ["id", "name", "email", "phone"], display_rows)
            for c in customers_data:
                cursor.execute(
                    "INSERT INTO customers (id, name, email, phone) VALUES (%s, %s, %s, %s)",
                    (c['id'], c['name'], c['email'], c['phone'])
                )
        
        payments_data = load_csv('db/data/payments.csv')
        if payments_data:
            display_rows = [[p['id'], p['customer_id'], p['card_number']] for p in payments_data]
            print_table("Restoring Payments", ["id", "customer_id", "card_number"], display_rows)
            for p in payments_data:
                cursor.execute(
                    "INSERT INTO payments (id, customer_id, card_number, amount) VALUES (%s, %s, %s, %s)",
                    (p['id'], p['customer_id'], p['card_number'], p['amount'])
                )
        
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
