import oracledb

from maskopy import mask_email, mask_phone, mask_card

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

def run_masking():
    config = {
        'user': 'maskopy',
        'password': 'maskopypwd',
        'dsn': 'localhost:1521/FREEPDB1'
    }
    
    try:
        conn = oracledb.connect(**config)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, email, phone FROM customers")
        columns = [col[0].lower() for col in cursor.description]
        customers = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        customer_rows = []
        for c in customers:
            new_email = mask_email(c['email'])
            new_phone = mask_phone(c['phone'])
            customer_rows.append([c['id'], c['name'], new_email, new_phone])
            cursor.execute(
                "UPDATE customers SET email=:1, phone=:2 WHERE id=:3",
                (new_email, new_phone, c['id'])
            )
        
        print_table("Masked Customers", ["id", "name", "email", "phone"], customer_rows)
        
        cursor.execute("SELECT id, customer_id, card_number FROM payments")
        columns = [col[0].lower() for col in cursor.description]
        payments = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        payment_rows = []
        for p in payments:
            new_card = mask_card(p['card_number'])
            payment_rows.append([p['id'], p['customer_id'], new_card])
            cursor.execute(
                "UPDATE payments SET card_number=:1 WHERE id=:2",
                (new_card, p['id'])
            )
            
        print_table("Masked Payments", ["id", "customer_id", "card_number"], payment_rows)
        
        conn.commit()
        print("\nMasking complete.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    run_masking()
