# Online Shopping Transaction Analysis System

An intermediate Python + MySQL + Streamlit project for analysing individual online-shopping transactions.

## Features
- Product, order and order-item tables in MySQL
- Order totals calculated from `quantity * unit_price` in order items
- Average transaction value (completed orders only)
- Order-status and payment-method distributions
- Monthly order volume and product units sold
- Date/status/payment filters and CSV export

## Technology
Python, MySQL, Pandas, NumPy, Matplotlib, Streamlit.

## Quick start (VS Code)

1. Install Python 3.10+ and MySQL Server.
2. Open this folder in VS Code.
3. Create and activate a virtual environment:

   **Windows**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Copy `.env.example` to `.env` and enter your MySQL username/password.
6. Create and seed the database:
   ```bash
   python setup_database.py
   ```
7. Start the dashboard:
   ```bash
   streamlit run app.py
   ```
8. Open the local URL printed by Streamlit (usually http://localhost:8501).

## MySQL schema
The schema is also available in `sql/schema.sql`. The setup script creates the database and inserts sample data automatically.

## Calculation and status rules
- Each order total is the sum of its order-item line totals: `quantity * unit_price`.
- Completed orders are included in completed sales and average transaction value.
- Pending orders appear in order counts/status reporting but are excluded from completed sales and average transaction value.
- Cancelled and refunded orders are excluded from completed sales and average transaction value, but remain visible in the status report.
- The monthly order-volume chart counts all statuses that match the selected filters.
- Product units sold in the filtered report includes the selected orders' item quantities. For a strict net-sales interpretation, filter to Completed orders.

## Project boundary
This is transaction-level analysis only. It does not implement customer segmentation, customer lifetime value, or an executive/business KPI dashboard.

## GitHub upload

Create a new empty repository on GitHub, then run these commands in the VS Code terminal from this project folder:

```bash
git init
git add .
git commit -m "Initial commit: online shopping transaction analysis"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the remote URL with your own GitHub repository URL. Never commit your `.env` file or real database passwords.
