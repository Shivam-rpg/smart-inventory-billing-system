from database import conn


class Customers:
    def __init__(self, name=None, email=None, phone=None):
        self.name = name
        self.email = email
        self.phone = phone

    def create_table(self):
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                phone VARCHAR(15) NOT NULL
            )
        """)
        conn.commit()
        cur.close()

    def insert_customer(self):
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s)",
            (self.name, self.email, self.phone)
        )
        conn.commit()
        cur.close()

    def update_customer(self, customer_id, name=None, email=None, phone=None):
        cur = conn.cursor()
        cur.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
        customer = cur.fetchone()

        if not customer:
            cur.close()
            return False

        if name:
            cur.execute("UPDATE customers SET name = %s WHERE id = %s", (name, customer_id))
        if email:
            cur.execute("UPDATE customers SET email = %s WHERE id = %s", (email, customer_id))
        if phone:
            cur.execute("UPDATE customers SET phone = %s WHERE id = %s", (phone, customer_id))

        conn.commit()
        cur.close()
        return True

    def delete_customer(self, customer_id):
        cur = conn.cursor()
        cur.execute("DELETE FROM customers WHERE id = %s", (customer_id,))
        conn.commit()
        cur.close()

    def get_all_customers(self):
        cur = conn.cursor()
        cur.execute("SELECT * FROM customers ORDER BY id")
        customers = cur.fetchall()
        cur.close()
        return customers
                