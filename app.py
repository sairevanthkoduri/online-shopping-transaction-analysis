
import sqlite3
from pathlib import Path
from datetime import date, timedelta

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


# Database location
DB_PATH = Path(__file__).parent / "shopping_analysis.db"

st.set_page_config(
    page_title="Online Shopping Transaction Analysis",
    page_icon="🛒",
    layout="wide"
)

# ==========================================
# PROFESSIONAL DASHBOARD DESIGN
# ==========================================

st.markdown("""
<style>

/* Main application */
.stApp {
    background-color: #0B1120;
    color: #F8FAFC;
}

/* Main content spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #273449;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #F8FAFC;
}

/* Main headings */
h1, h2, h3 {
    color: #F8FAFC !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px;
}

/* KPI cards */
div[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        #172338,
        #111827
    );
    border: 1px solid #293B54;
    padding: 22px 20px;
    border-radius: 14px;
    box-shadow: 0 5px 18px rgba(0,0,0,0.15);
}

/* KPI labels */
div[data-testid="stMetricLabel"] {
    color: #A8B7CC !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}

/* KPI values */
div[data-testid="stMetricValue"] {
    color: #F8FAFC !important;
    font-size: 30px !important;
    font-weight: 700 !important;
}

/* Buttons */
.stButton > button {
    background: #2563EB;
    color: white;
    border: none;
    border-radius: 9px;
    padding: 10px 18px;
    font-weight: 600;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background: #1D4ED8;
    color: white;
    border: none;
}

/* Download button */
.stDownloadButton > button {
    background: #059669;
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: 600;
}

.stDownloadButton > button:hover {
    background: #047857;
    color: white;
    border: none;
}

/* Input fields */
.stSelectbox, .stMultiSelect,
.stDateInput, .stTextInput {
    border-radius: 9px;
}

/* Data tables */
div[data-testid="stDataFrame"] {
    border: 1px solid #293B54;
    border-radius: 12px;
    overflow: hidden;
}

/* Dividers */
hr {
    border-color: #293B54 !important;
}

/* Captions */
.stCaption {
    color: #94A3B8 !important;
}

/* Hide Streamlit footer and menu */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Success message */
div[data-testid="stAlert"] {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# Dark chart theme
plt.style.use("dark_background")


STATUSES = ["Completed", "Pending", "Cancelled", "Refunded"]

PAYMENTS = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Cash on Delivery",
    "Net Banking"
]


# Database connection
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# Load database records
def load_data():

    conn = get_connection()

    try:
        products = pd.read_sql_query(
            "SELECT * FROM products", conn
        )

        orders = pd.read_sql_query(
            "SELECT * FROM orders", conn
        )

        items = pd.read_sql_query("""
            SELECT
                oi.item_id,
                oi.order_id,
                oi.product_id,
                p.product_name,
                p.category,
                oi.quantity,
                oi.unit_price,
                (oi.quantity * oi.unit_price) AS line_total

            FROM order_items oi

            JOIN products p
            ON p.product_id = oi.product_id
        """, conn)

        return products, orders, items

    finally:
        conn.close()


# Currency formatting
def money(value):
    return f"₹{value:,.2f}"


# Dashboard title

# Professional Dashboard Header

st.html("""
<div style="
    padding: 10px 0 25px 0;
">
    <div style="
        color: #60A5FA;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 8px;
    ">
        E-COMMERCE INTELLIGENCE
    </div>

    <div style="
        color: #F8FAFC;
        font-size: 34px;
        font-weight: 800;
        letter-spacing: -1px;
    ">
        🛒 Online Shopping Analytics
    </div>

    <div style="
        color: #94A3B8;
        font-size: 15px;
        margin-top: 8px;
    ">
        Monitor transactions, revenue, customer purchasing
        patterns and product performance.
    </div>
</div>
""")

st.divider()



# Sidebar
with st.sidebar:

    st.header("Database")

    st.success("SQLite Database Connected")

    st.write("Database: shopping_analysis.db")

    if st.button("Refresh data",width="stretch"):
        st.rerun()

    st.divider()

    st.markdown("**Order treatment**")

    st.caption(
        "Completed orders are included in sales-value "
        "and average-order-value calculations. "
        "Pending orders are shown in status/volume reports "
        "but excluded from completed-sales value. "
        "Cancelled and refunded orders are excluded "
        "from sales value."
    )


# Load data
try:

    products, orders, items = load_data()

except Exception as e:

    st.error("Could not load data from SQLite database.")

    st.code(str(e))

    st.info(
        "Run python setup_database.py "
        "to create the database."
    )

    st.stop()


# Check orders
if orders.empty:

    st.warning("No orders found in the database.")

    st.stop()


# Convert order date
orders["order_date"] = pd.to_datetime(
    orders["order_date"]
)


# Calculate order value
order_totals = (
    items.groupby("order_id", as_index=False)["line_total"]
    .sum()
    .rename(columns={"line_total": "order_value"})
)

orders = orders.merge(
    order_totals,
    on="order_id",
    how="left"
)

orders["order_value"] = orders["order_value"].fillna(0)


# Completed orders
completed = orders[
    orders["order_status"].str.lower() == "completed"
].copy()


# Date filters
min_date = orders["order_date"].min().date()
max_date = orders["order_date"].max().date()


with st.sidebar:

    st.subheader("Filters")

    date_range = st.date_input(
        "Order date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if len(date_range) == 2:

        start_date, end_date = date_range

    else:

        start_date = date_range[0]
        end_date = date_range[0]


    status_filter = st.multiselect(
        "Order status",
        STATUSES,
        default=STATUSES
    )

    available_payments = sorted(
        orders["payment_method"].dropna().unique()
    )

    payment_filter = st.multiselect(
        "Payment method",
        available_payments,
        default=available_payments
    )


# Apply filters
filtered = orders[
    orders["order_date"].dt.date.between(
        start_date, end_date
    )
    & orders["order_status"].isin(status_filter)
    & orders["payment_method"].isin(payment_filter)
]


filtered_completed = filtered[
    filtered["order_status"].str.lower() == "completed"
]


filtered_ids = filtered["order_id"].tolist()

filtered_items = items[
    items["order_id"].isin(filtered_ids)
]


# Calculate KPIs
total_orders = len(filtered)

completed_count = len(filtered_completed)

completed_revenue = filtered_completed[
    "order_value"
].sum()

aov = (
    completed_revenue / completed_count
    if completed_count else 0
)

units = filtered_items["quantity"].sum()


# Display metrics
st.subheader("Key Performance Indicators")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Orders",
    f"{total_orders:,}"
)

c2.metric(
    "Completed Sales",
    money(completed_revenue)
)

c3.metric(
    "Average Transaction Value",
    money(aov)
)

c4.metric(
    "Product Units Sold",
    f"{int(units):,}"
)


st.divider()


# Order status and payment analysis
left, right = st.columns(2)


with left:

    st.subheader("Order Status Distribution")

    status_counts = (
        filtered["order_status"]
        .value_counts()
        .reindex(STATUSES, fill_value=0)
    )

    fig, ax = plt.subplots()
    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#111827")
    ax.tick_params(colors="#CBD5E1")
    ax.xaxis.label.set_color("#CBD5E1")
    ax.yaxis.label.set_color("#CBD5E1")
    ax.title.set_color("#F8F9FC")

    status_counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Order Status")
    ax.set_ylabel("Number of Orders")

    ax.tick_params(
        axis="x",
        rotation=25
    )

    st.pyplot(fig)

    plt.close(fig)


with right:

    st.subheader("Payment Method Distribution")

    payment_counts = filtered[
        "payment_method"
    ].value_counts()

    fig, ax = plt.subplots()
    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#111827")

    ax.tick_params(colors="#CBD5E1")
    ax.xaxis.label.set_color("#CBD5E1")
    ax.yaxis.label.set_color("#CBD5E1")
    ax.title.set_color("#F8FAFC")

    if len(payment_counts):

        payment_counts.plot(
    kind="pie",
    autopct="%1.1f%%",
    ax=ax,
    ylabel="",
    textprops={"color": "#F8FAFC", "fontsize": 11}
)

    else:

        ax.text(
            0.5,
            0.5,
            "No orders for selected filters",
            ha="center",
            va="center"
        )

        ax.axis("off")

    st.pyplot(fig)

    plt.close(fig)


st.divider()


# Monthly order volume and product analysis
left, right = st.columns(2)


with left:

    st.subheader("Monthly Order Volume")

    monthly = (
        filtered.set_index("order_date")
        .resample("MS")["order_id"]
        .count()
    )

    fig, ax = plt.subplots(figsize=(10, 4))

fig.patch.set_facecolor("#111827")
ax.set_facecolor("#111827")

monthly.plot(
    kind="line",
    marker="o",
    linewidth=2.5,
    markersize=7,
    color="#38BDF8",
    ax=ax
)

ax.set_title(
    "Monthly Order Volume",
    color="#F8FAFC",
    fontsize=15,
    fontweight="bold",
    pad=15
)
ax.set_xlabel("Month", color="#CBD5E1")
ax.set_ylabel("Number of Orders", color="#CBD5E1")

ax.tick_params(colors="#CBD5E1")
ax.grid(True, color="#334155", alpha=0.4)

for spine in ax.spines.values():
    spine.set_color("#334155")

fig.tight_layout()

st.pyplot(fig)

plt.close(fig)


with right:

    st.subheader("Product Units Sold")

    product_units = (
        filtered_items.groupby("product_name")["quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots()

    product_units.sort_values().plot(
        kind="barh",
        ax=ax
    )

    ax.set_xlabel("Units")
    ax.set_ylabel("Product")

    st.pyplot(fig)

    plt.close(fig)


st.divider()


# Transaction summary
st.subheader("Transaction Summary")

summary = filtered[
    [
        "order_id",
        "order_date",
        "payment_method",
        "order_status",
        "order_value"
    ]
].copy()

summary["order_date"] = (
    summary["order_date"].dt.strftime("%Y-%m-%d")
)

summary["order_value"] = (
    summary["order_value"].round(2)
)

st.dataframe(
    summary.sort_values(
        "order_date",
        ascending=False
    ),
    width="stretch",
    hide_index=True
)


# Order item details
st.subheader("Order Item Details")

detail = filtered_items[
    [
        "order_id",
        "product_name",
        "category",
        "quantity",
        "unit_price",
        "line_total"
    ]
].copy()

st.dataframe(
    detail,
    width="stretch",
    hide_index=True
)


# Download CSV
st.download_button(
    "Download Transaction Summary (CSV)",
    summary.to_csv(index=False).encode("utf-8"),
    "transaction_summary.csv",
    "text/csv"
)


# Footer
st.caption(
    "Built with Python, Streamlit, SQLite, "
    "Pandas, NumPy and Matplotlib."
)
