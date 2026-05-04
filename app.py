import streamlit as st
import pandas as pd
from datetime import date

from database import conn
from customers import Customers
from products import Products
from sales import Sales
from sale_items import SaleItems


# ---------------- INITIALIZE TABLES ---------------- #
def initialize_tables():
    try:
        Customers().create_table()
        Products().create_table()
        Sales().create_table()
        SaleItems().create_table()

        cur = conn.cursor()
        cur.execute("SELECT setval('customers_id_seq', COALESCE((SELECT MAX(id) FROM customers),1))")
        cur.execute("SELECT setval('products_id_seq', COALESCE((SELECT MAX(id) FROM products),1))")
        cur.execute("SELECT setval('sales_id_seq', COALESCE((SELECT MAX(id) FROM sales),1))")
        cur.execute("SELECT setval('sale_items_id_seq', COALESCE((SELECT MAX(id) FROM sale_items),1))")
        conn.commit()
        cur.close()

    except Exception as e:
        st.error(f"Database Initialization Error: {e}")


# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(page_title="Smart Inventory and Billing System", layout="wide")
st.title("Smart Inventory and Billing System")

if "tables_initialized" not in st.session_state:
    initialize_tables()
    st.session_state.tables_initialized = True


# ---------------- SIDEBAR ---------------- #
st.sidebar.header("Navigation")
menu_option = st.sidebar.selectbox(
    "Select a Section",
    [
        "Dashboard",
        "Customers Management",
        "Products Management",
        "Sales Management",
        "Analytics and Reports"
    ]
)


# ---------------- DASHBOARD ---------------- #
if menu_option == "Dashboard":
    st.subheader("Dashboard Overview")

    try:
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM customers")
        customer_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM products")
        product_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM sales")
        sales_count = cur.fetchone()[0]

        cur.execute("SELECT COALESCE(SUM(total_amount),0) FROM sales")
        total_revenue = cur.fetchone()[0]

        cur.close()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Customers", customer_count)
        col2.metric("Total Products", product_count)
        col3.metric("Total Orders", sales_count)
        col4.metric("Total Revenue", f"₹{total_revenue}")

    except Exception as e:
        st.warning(f"Dashboard Data Error: {e}")


# ---------------- CUSTOMERS MANAGEMENT ---------------- #
elif menu_option == "Customers Management":
    st.subheader("Customers Management")

    tab1, tab2, tab3, tab4 = st.tabs(["Add Customer", "View Customers", "Update Customer", "Delete Customer"])

    with tab1:
        with st.form("add_customer"):
            name = st.text_input("Customer Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            submit = st.form_submit_button("Add Customer")

            if submit:
                Customers(name, email, phone).insert_customer()
                st.success("Customer Added Successfully")

    with tab2:
        customers = Customers().get_all_customers()
        if customers:
            df = pd.DataFrame(customers, columns=["ID", "Name", "Email", "Phone"])
            st.dataframe(df, use_container_width=True)

    with tab3:
        with st.form("update_customer"):
            customer_id = st.number_input("Customer ID", min_value=1)
            new_name = st.text_input("New Name")
            new_email = st.text_input("New Email")
            new_phone = st.text_input("New Phone")
            update_submit = st.form_submit_button("Update Customer")

            if update_submit:
                status = Customers().update_customer(customer_id, new_name, new_email, new_phone)
                if status:
                    st.success("Customer Updated Successfully")
                else:
                    st.error("Customer ID Not Found")

    with tab4:
        customer_id = st.number_input("Customer ID to Delete", min_value=1, key="delete_customer")
        if st.button("Delete Customer"):
            Customers().delete_customer(customer_id)
            st.success("Customer Deleted Successfully")


# ---------------- PRODUCTS MANAGEMENT ---------------- #
elif menu_option == "Products Management":
    st.subheader("Products Management")

    tab1, tab2, tab3, tab4 = st.tabs(["Add Product", "View Products", "Update Product", "Delete Product"])

    with tab1:
        with st.form("add_product"):
            name = st.text_input("Product Name")
            description = st.text_input("Description")
            quantity = st.number_input("Quantity", min_value=1)
            price = st.number_input("Price", min_value=1.0)
            submit = st.form_submit_button("Add Product")

            if submit:
                Products(name, description, quantity, price).insert_product()
                st.success("Product Added Successfully")

    with tab2:
        products = Products().get_all_products()
        if products:
            df = pd.DataFrame(products, columns=["ID", "Name", "Description", "Quantity", "Price"])
            st.dataframe(df, use_container_width=True)

    with tab3:
        with st.form("update_product"):
            product_id = st.number_input("Product ID", min_value=1)
            new_name = st.text_input("New Product Name")
            new_description = st.text_input("New Description")
            new_quantity = st.number_input("New Quantity", min_value=0)
            new_price = st.number_input("New Price", min_value=0.0)
            update_submit = st.form_submit_button("Update Product")

            if update_submit:
                status = Products().update_product(product_id, new_name, new_description, new_quantity, new_price)
                if status:
                    st.success("Product Updated Successfully")
                else:
                    st.error("Product ID Not Found")

    with tab4:
        product_id = st.number_input("Product ID to Delete", min_value=1, key="delete_product")
        if st.button("Delete Product"):
            Products().delete_product(product_id)
            st.success("Product Deleted Successfully")


# ---------------- SALES MANAGEMENT ---------------- #
elif menu_option == "Sales Management":
    st.subheader("Sales Management")

    tab1, tab2, tab3 = st.tabs(["Create Sale", "View Sales", "Delete Sale"])

    with tab1:
        cur = conn.cursor()

        cur.execute("SELECT id, name FROM customers")
        customer_data = cur.fetchall()

        cur.execute("SELECT id, name, price, quantity FROM products")
        product_data = cur.fetchall()
        cur.close()

        if customer_data and product_data:
            customer_dict = {f"{row[0]} - {row[1]}": row[0] for row in customer_data}
            product_dict = {f"{row[0]} - {row[1]}": (row[0], row[2], row[3]) for row in product_data}

            selected_customer = st.selectbox("Select Customer", list(customer_dict.keys()))
            selected_product = st.selectbox("Select Product", list(product_dict.keys()))
            quantity = st.number_input("Quantity to Buy", min_value=1)

            product_id, product_price, stock_qty = product_dict[selected_product]
            total_amount = product_price * quantity

            st.info(f"Available Stock: {stock_qty}")
            st.info(f"Total Bill Amount: ₹{total_amount}")

            if st.button("Generate Sale"):
                if quantity > stock_qty:
                    st.error("Not enough stock available.")
                else:
                    customer_id = customer_dict[selected_customer]
                    cur = conn.cursor()

                    cur.execute(
                        "INSERT INTO sales (customer_id, date, total_amount) VALUES (%s, %s, %s) RETURNING id",
                        (customer_id, date.today(), total_amount)
                    )
                    sale_id = cur.fetchone()[0]

                    cur.execute(
                        "INSERT INTO sale_items (sale_id, product_id, quantity) VALUES (%s, %s, %s)",
                        (sale_id, product_id, quantity)
                    )

                    cur.execute(
                        "UPDATE products SET quantity = quantity - %s WHERE id = %s",
                        (quantity, product_id)
                    )

                    conn.commit()
                    cur.close()

                    st.success(f"Sale Generated Successfully | Sale ID = {sale_id}")
        else:
            st.warning("Please Add Customers and Products First.")

    with tab2:
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                s.id,
                c.name,
                p.name,
                si.quantity,
                p.price,
                s.total_amount,
                s.date
            FROM sales s
            JOIN customers c ON s.customer_id = c.id
            JOIN sale_items si ON s.id = si.sale_id
            JOIN products p ON si.product_id = p.id
            ORDER BY s.id
        """)
        sales = cur.fetchall()
        cur.close()

        if sales:
            df = pd.DataFrame(sales, columns=["Sale ID", "Customer", "Product", "Qty", "Unit Price", "Total", "Date"])
            st.dataframe(df, use_container_width=True)

    with tab3:
        sale_id = st.number_input("Sale ID to Delete", min_value=1, key="delete_sale")
        if st.button("Delete Sale"):
            Sales().delete_sale(sale_id)
            st.success("Sale Deleted Successfully and Stock Restored")


# ---------------- ANALYTICS ---------------- #
elif menu_option == "Analytics and Reports":
    st.subheader("Analytics and Reports")

    cur = conn.cursor()

    cur.execute("SELECT date, SUM(total_amount) FROM sales GROUP BY date ORDER BY date")
    sales_trend = cur.fetchall()

    cur.execute("""
        SELECT p.name, SUM(si.quantity)
        FROM sale_items si
        JOIN products p ON si.product_id = p.id
        GROUP BY p.name
        ORDER BY SUM(si.quantity) DESC
        LIMIT 5
    """)
    top_products = cur.fetchall()

    cur.execute("""
        SELECT c.name, SUM(s.total_amount)
        FROM sales s
        JOIN customers c ON s.customer_id = c.id
        GROUP BY c.name
        ORDER BY SUM(s.total_amount) DESC
        LIMIT 5
    """)
    top_customers = cur.fetchall()
    cur.close()

    st.write("### Daily Sales Trend")
    if sales_trend:
        df = pd.DataFrame(sales_trend, columns=["Date", "Revenue"])
        st.line_chart(df.set_index("Date"), height=250)

    st.write("### Top 5 Selling Products")
    if top_products:
        df2 = pd.DataFrame(top_products, columns=["Product", "Quantity Sold"])
        st.bar_chart(df2.set_index("Product"))

    st.write("### Top Customers by Spending")
    if top_customers:
        df3 = pd.DataFrame(top_customers, columns=["Customer", "Spent"])
        st.dataframe(df3, use_container_width=True)