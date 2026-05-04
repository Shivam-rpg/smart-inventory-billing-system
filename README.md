# Smart Inventory and Billing System

A full-stack database-driven Inventory and Billing Management application developed using **Python, PostgreSQL, and Streamlit**.  
This project helps businesses efficiently manage **customers, products, sales transactions, stock updates, billing operations, and analytical reports** through an interactive web dashboard.

---

## Project Overview

The Smart Inventory and Billing System is designed to automate the daily operations of a small business/shop by replacing manual record keeping with a centralized digital solution.

The system provides:

- Real-time customer records management
- Product inventory management
- Sales generation with automatic bill amount calculation
- Automatic stock deduction after each sale
- Stock restoration on sale deletion
- Revenue analytics and customer spending reports

---

## Key Features

### Customer Management
- Add New Customers
- View Existing Customers
- Update Customer Information
- Delete Customers

### Product Management
- Add New Products
- View Product Inventory
- Update Product Details
- Delete Products

### Sales Management
- Generate New Sale
- Automatic Total Bill Calculation
- Automatic Quantity Deduction from Inventory
- View All Sales Transactions
- Delete Sale with Automatic Stock Recovery

### Analytics Dashboard
- Daily Sales Revenue Trend
- Top 5 Selling Products
- Top Customers by Spending
- Dashboard KPI Metrics

---

## Tech Stack Used

| Technology | Purpose |
|------------|---------|
| Python | Core Backend Logic |
| PostgreSQL | Relational Database |
| Streamlit | Interactive Web Application UI |
| Pandas | Data Handling & Reports |
| Psycopg2 | PostgreSQL Database Connectivity |
| Python Dotenv | Environment Variable Security |

---

## Project Structure

smart-inventory-billing-system/
│
├── app.py
├── database.py
├── customers.py
├── products.py
├── sales.py
├── sale_items.py
├── database_schema.sql
├── requirements.txt
├── .gitignore
└── README.md

---

## Database Schema

The project uses four relational tables:

- customers
- products
- sales
- sale_items

These tables are connected using foreign key relationships to maintain proper transactional consistency.

---

## Environment Configuration

Create a `.env` file in the root directory and add the following credentials:

```env
DB_HOST=localhost
DB_NAME=ecommerce
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432
