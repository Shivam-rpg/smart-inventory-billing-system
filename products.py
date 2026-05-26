from database import get_connection


class Products:
    def __init__(self, name=None, description=None, quantity=None, price=None):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.price = price

    def create_table(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                quantity INT,
                price NUMERIC(10,2)
            )
        """)

        conn.commit()

        cur.close()
        conn.close()

    def insert_product(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO products 
            (name, description, quantity, price)
            VALUES (%s, %s, %s, %s)
            """,
            (self.name, self.description, self.quantity, self.price)
        )

        conn.commit()

        cur.close()
        conn.close()

    def update_product(self, product_id, name=None, description=None, quantity=None, price=None):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        product = cur.fetchone()

        if not product:
            cur.close()
            conn.close()
            return False

        if name:
            cur.execute(
                "UPDATE products SET name = %s WHERE id = %s",
                (name, product_id)
            )

        if description:
            cur.execute(
                "UPDATE products SET description = %s WHERE id = %s",
                (description, product_id)
            )

        if quantity is not None:
            cur.execute(
                "UPDATE products SET quantity = %s WHERE id = %s",
                (quantity, product_id)
            )

        if price is not None:
            cur.execute(
                "UPDATE products SET price = %s WHERE id = %s",
                (price, product_id)
            )

        conn.commit()

        cur.close()
        conn.close()

        return True

    def delete_product(self, product_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM products WHERE id = %s",
            (product_id,)
        )

        conn.commit()

        cur.close()
        conn.close()

    def get_all_products(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM products ORDER BY id")
        products = cur.fetchall()

        cur.close()
        conn.close()

        return products