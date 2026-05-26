# Smart Inventory and Billing System

A full-stack Inventory and Billing Management System developed using Python, PostgreSQL, and Streamlit.  
The project helps businesses manage customers, products, sales transactions, inventory tracking, and business analytics through an interactive dashboard.

---

# Project Overview

The Smart Inventory and Billing System automates daily shop/business operations by replacing manual billing and inventory handling with a centralized database-driven solution.

The system provides:

- Customer records management
- Product inventory management
- Sales and billing operations
- Automatic stock quantity updates
- Revenue analytics and reporting
- Real-time PostgreSQL database integration

---

## Analytics Dashboard

- Daily Revenue Trend
- Top Selling Products
- Top Customers by Spending
- KPI Dashboard Metrics

---

# Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Backend Development |
| PostgreSQL | Relational Database |
| Streamlit | Interactive Web UI |
| Pandas | Data Handling |
| Psycopg2 | PostgreSQL Connectivity |
| Python Dotenv | Environment Variable Management |

---

# Project Structure

```bash
smart-inventory-billing-system/
│
├── app.py
├── customers.py
├── products.py
├── sales.py
├── sale_items.py
├── database.py
├── database_schema.sql
├── requirements.txt
├── .gitignore
├── README.md
└── .env
```

# Database Relationships

- `sales.customer_id → customers.id`
- `sale_items.sale_id → sales.id`
- `sale_items.product_id → products.id`

The project uses:

- Foreign Key Constraints
- ON DELETE CASCADE
- Relational SQL Queries
- Aggregate Queries
- Inventory Stock Transactions

---

# Environment Variables

Create a `.env` file in the root directory.

```env
DB_HOST=your_host
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
DB_PORT=5432
```


---

# Security Features

- Environment Variables using `.env`
- Secure PostgreSQL Connection
- SSL Database Connection
- Dynamic Database Connections
- Prevention of Global Connection Failures

---

# Future Improvements

- User Authentication System
- Invoice PDF Generation
- GST Billing
- Multi-user Access
- Export Reports to Excel/PDF
- Advanced Analytics Dashboard

---

# Live Link

https://smart-inventory-billing-system-nt24.streamlit.app/

# Author

Shivam Patel

B.Tech Electronics and Communication Engineering  
Data Analytics & Python Developer

---

# License

This project is developed for educational and portfolio purposes.
