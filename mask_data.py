import mysql.connector
from maskopy import mask_email, mask_phone, mask_card

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

def run_masking():
    config = {
        'host': '127.0.0.1',
        'port': 3307,
        'user': 'root',
        'password': 'rootpwd',
        'database': 'dummy_db'
    }
    
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)
        
        # Mask Customers
        cursor.execute("SELECT id, name, email, phone FROM customers")
        customers = cursor.fetchall()
        
        customer_rows = []
        for c in customers:
            new_email = mask_email(c['email'])
            new_phone = mask_phone(c['phone'])
            customer_rows.append([c['id'], c['name'], new_email, new_phone])
            cursor.execute(
                "UPDATE customers SET email=%s, phone=%s WHERE id=%s",
                (new_email, new_phone, c['id'])
            )
        
        print_table("Masked Customers", ["id", "name", "email", "phone"], customer_rows)
        
        # Mask Payments
        cursor.execute("SELECT id, customer_id, card_number FROM payments")
        payments = cursor.fetchall()
        
        payment_rows = []
        for p in payments:
            new_card = mask_card(p['card_number'])
            payment_rows.append([p['id'], p['customer_id'], new_card])
            cursor.execute(
                "UPDATE payments SET card_number=%s WHERE id=%s",
                (new_card, p['id'])
            )
            
        print_table("Masked Payments", ["id", "customer_id", "card_number"], payment_rows)
        
        conn.commit()
        print("\nMasking complete.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    run_masking()
