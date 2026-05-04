from database import conn


class Sales:
    def __init__(self, customer_id=None, date=None, total_amount=None):
        self.customer_id = customer_id
        self.date = date
        self.total_amount = total_amount

    def create_table(self):
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id SERIAL PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                date DATE NOT NULL,
                total_amount NUMERIC(10,2) NOT NULL,
                CONSTRAINT fk_sales_customer
                FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
            )
        """)
        conn.commit()
        cur.close()

    def insert_sale(self):
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO sales (customer_id, date, total_amount) VALUES (%s, %s, %s)",
            (self.customer_id, self.date, self.total_amount)
        )
        conn.commit()
        cur.close()

    def get_all_sales(self):
        cur = conn.cursor()
        cur.execute("SELECT * FROM sales ORDER BY id")
        sales = cur.fetchall()
        cur.close()
        return sales

    def delete_sale(self, sale_id):
        cur = conn.cursor()

        # restore stock before deleting sale
        cur.execute("""
            SELECT product_id, quantity
            FROM sale_items
            WHERE sale_id = %s
        """, (sale_id,))
        sale_products = cur.fetchall()

        for product_id, qty in sale_products:
            cur.execute("""
                UPDATE products
                SET quantity = quantity + %s
                WHERE id = %s
            """, (qty, product_id))

        cur.execute("DELETE FROM sales WHERE id = %s", (sale_id,))
        conn.commit()
        cur.close()

    def view_sale_by_id(self, sale_id):
        cur = conn.cursor()
        cur.execute("SELECT * FROM sales WHERE id = %s", (sale_id,))
        sale = cur.fetchone()
        cur.close()
        return sale