from database import get_connection


class SaleItems:
    def __init__(self, sale_id=None, product_id=None, quantity=None):
        self.sale_id = sale_id
        self.product_id = product_id
        self.quantity = quantity

    def create_table(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS sale_items (
                id SERIAL PRIMARY KEY,

                sale_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,

                CONSTRAINT fk_sale_items_sale
                FOREIGN KEY (sale_id)
                REFERENCES sales(id)
                ON DELETE CASCADE,

                CONSTRAINT fk_sale_items_product
                FOREIGN KEY (product_id)
                REFERENCES products(id)
                ON DELETE CASCADE
            )
        """)

        conn.commit()

        cur.close()
        conn.close()

    def insert_sale_item(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO sale_items
            (sale_id, product_id, quantity)
            VALUES (%s, %s, %s)
            """,
            (self.sale_id, self.product_id, self.quantity)
        )

        conn.commit()

        cur.close()
        conn.close()