import streamlit as st
import pandas as pd
import plotly.express as px

from utils.load_data import load_data

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Embedded Finance Revenue Analytics",
    page_icon="💳",
    layout="wide"
)

# =====================================================
# Load Data
# =====================================================

customers, products, partners, transactions, funnel = load_data()

# =====================================================
# Sidebar Filters
# =====================================================

st.sidebar.title("Filters")

selected_product = st.sidebar.multiselect(
    "Product",
    options=products["product_name"].unique(),
    default=products["product_name"].unique()
)

selected_partner = st.sidebar.multiselect(
    "Partner",
    options=partners["partner_name"].unique(),
    default=partners["partner_name"].unique()
)

date_range = st.sidebar.date_input(
    "Transaction Date",
    value=(
        transactions["transaction_date"].min().date(),
        transactions["transaction_date"].max().date()
    )
)

# =====================================================
# Merge Tables
# =====================================================

transactions = transactions.merge(
    products[["product_id", "product_name"]],
    on="product_id",
    how="left"
)

transactions = transactions.merge(
    partners[["partner_id", "partner_name"]],
    on="partner_id",
    how="left"
)

# =====================================================
# Apply Filters
# =====================================================

filtered = transactions.copy()

filtered = filtered[
    filtered["product_name"].isin(selected_product)
]

filtered = filtered[
    filtered["partner_name"].isin(selected_partner)
]

if len(date_range) == 2:

    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    filtered = filtered[
        (filtered["transaction_date"] >= start_date)
        &
        (filtered["transaction_date"] <= end_date)
    ]

# =====================================================
# Dashboard Title
# =====================================================

st.title("💳 Embedded Finance Revenue Analytics")

st.markdown("### Executive Dashboard")

# =====================================================
# KPI Calculations
# =====================================================

total_revenue = filtered["revenue"].sum()

total_customers = filtered["customer_id"].nunique()

total_transactions = filtered["transaction_id"].count()

average_cltv = (
    total_revenue / total_customers
    if total_customers > 0
    else 0
)

# =====================================================
# KPI Cards
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Total Revenue",
        f"${total_revenue:,.2f}"
    )

with col2:
    st.metric(
        "👥 Total Customers",
        f"{total_customers:,}"
    )

with col3:
    st.metric(
        "💳 Total Transactions",
        f"{total_transactions:,}"
    )

with col4:
    st.metric(
        "📈 Average CLTV",
        f"${average_cltv:,.2f}"
    )

# =====================================================
# Monthly Revenue Trend
# =====================================================

monthly_revenue = (
    filtered
    .groupby(filtered["transaction_date"].dt.to_period("M"))["revenue"]
    .sum()
    .reset_index()
)

monthly_revenue["transaction_date"] = (
    monthly_revenue["transaction_date"]
    .astype(str)
)

line_fig = px.line(
    monthly_revenue,
    x="transaction_date",
    y="revenue",
    title="Monthly Revenue Trend",
    markers=True
)

line_fig.update_layout(
    template="plotly_white",
    hovermode="x unified",
    xaxis_title="Month",
    yaxis_title="Revenue ($)"
)

st.plotly_chart(
    line_fig,
    use_container_width=True
)

# =====================================================
# Revenue by Product
# =====================================================

product_revenue = (
    filtered
    .groupby("product_name")["revenue"]
    .sum()
    .reset_index()
    .sort_values(by="revenue", ascending=False)
)

product_fig = px.bar(
    product_revenue,
    x="product_name",
    y="revenue",
    title="Revenue by Product",
    color="revenue",
    text_auto=".2s"
)

product_fig.update_layout(
    template="plotly_white",
    xaxis_title="Product",
    yaxis_title="Revenue ($)"
)

product_fig.update_traces(
    textposition="outside"
)

# =====================================================
# Revenue by Partner
# =====================================================

partner_revenue = (
    filtered
    .groupby("partner_name")["revenue"]
    .sum()
    .reset_index()
    .sort_values(by="revenue", ascending=False)
)

partner_fig = px.bar(
    partner_revenue,
    x="partner_name",
    y="revenue",
    title="Revenue by Partner",
    color="revenue",
    text_auto=".2s"
)

partner_fig.update_layout(
    template="plotly_white",
    xaxis_title="Partner",
    yaxis_title="Revenue ($)"
)

partner_fig.update_traces(
    textposition="outside"
)

# =====================================================
# Side-by-Side Charts
# =====================================================

left_col, right_col = st.columns(2)

with left_col:
    st.plotly_chart(
        product_fig,
        use_container_width=True
    )

with right_col:
    st.plotly_chart(
        partner_fig,
        use_container_width=True
    )
    # =====================================================
# Product Adoption Analysis
# =====================================================

st.markdown("---")
st.subheader("📦 Product Adoption Analysis")

product_adoption = (
    filtered
    .groupby("product_name")["customer_id"]
    .nunique()
    .reset_index(name="customers")
    .sort_values("customers", ascending=True)
)

adoption_fig = px.bar(
    product_adoption,
    x="customers",
    y="product_name",
    orientation="h",
    title="Unique Customers by Product",
    text="customers",
    color="customers",
    color_continuous_scale="Blues"
)

adoption_fig.update_layout(
    template="plotly_white",
    xaxis_title="Unique Customers",
    yaxis_title="Product"
)

st.plotly_chart(
    adoption_fig,
    use_container_width=True
)
# =====================================================
# Cross-Sell Success Analysis
# =====================================================

st.markdown("---")
st.subheader("🔄 Cross-Sell Success Analysis")

# Count unique products used by each customer
customer_products = (
    filtered
    .groupby("customer_id")["product_id"]
    .nunique()
    .reset_index(name="product_count")
)

# Categorize customers
customer_products["Category"] = customer_products["product_count"].apply(
    lambda x: "Multi Product" if x > 1 else "Single Product"
)

# Count customers in each category
cross_sell = (
    customer_products
    .groupby("Category")
    .size()
    .reset_index(name="Customers")
)

# Calculate cross-sell rate
total_customers = customer_products.shape[0]
multi_product_customers = customer_products[
    customer_products["product_count"] > 1
].shape[0]

cross_sell_rate = (
    multi_product_customers / total_customers * 100
    if total_customers > 0 else 0
)
metric1, metric2 = st.columns(2)

with metric1:
    st.metric(
        "Cross-Sell Rate",
        f"{cross_sell_rate:.1f}%"
    )

with metric2:
    st.metric(
        "Multi-Product Customers",
        multi_product_customers
    )
    cross_sell_fig = px.pie(
    cross_sell,
    names="Category",
    values="Customers",
    hole=0.6,
    title="Single vs Multi-Product Customers"
)

cross_sell_fig.update_layout(
    template="plotly_white"
)

st.plotly_chart(
    cross_sell_fig,
    use_container_width=True
)
# =====================================================
# Repeat Usage Analysis
# =====================================================

st.markdown("---")
st.subheader("🔁 Repeat Usage Analysis")

customer_transactions = (
    filtered
    .groupby("customer_id")
    .size()
    .reset_index(name="transaction_count")
)

customer_transactions["Category"] = customer_transactions[
    "transaction_count"
].apply(
    lambda x: "Repeat User" if x > 1 else "One-Time User"
)

repeat_summary = (
    customer_transactions
    .groupby("Category")
    .size()
    .reset_index(name="Customers")
)

repeat_users = customer_transactions[
    customer_transactions["transaction_count"] > 1
].shape[0]

one_time_users = customer_transactions[
    customer_transactions["transaction_count"] == 1
].shape[0]

repeat_rate = (
    repeat_users /
    len(customer_transactions) * 100
    if len(customer_transactions) > 0 else 0
)
repeat_col1, repeat_col2, repeat_col3 = st.columns(3)

with repeat_col1:
    st.metric(
        "Repeat Usage Rate",
        f"{repeat_rate:.1f}%"
    )

with repeat_col2:
    st.metric(
        "Repeat Users",
        repeat_users
    )

with repeat_col3:
    st.metric(
        "One-Time Users",
        one_time_users
    )
    repeat_fig = px.bar(
    repeat_summary,
    x="Category",
    y="Customers",
    color="Category",
    text="Customers",
    title="Repeat vs One-Time Users"
)

repeat_fig.update_layout(
    template="plotly_white",
    xaxis_title="Customer Type",
    yaxis_title="Number of Customers",
    showlegend=False
)

repeat_fig.update_traces(
    textposition="outside"
)

st.plotly_chart(
    repeat_fig,
    use_container_width=True
)
# =====================================================
# Funnel Conversion Analysis
# =====================================================

st.markdown("---")
st.subheader("🎯 Funnel Conversion & Drop-Off")

funnel_order = [
    "Viewed",
    "Application Started",
    "KYC Completed",
    "Approved",
    "Activated",
    "First Transaction"
]

funnel_data = (
    funnel.groupby("stage")["customer_id"]
    .nunique()
    .reindex(funnel_order)
    .reset_index()
)

funnel_data.columns = ["Stage", "Customers"]
funnel_data["Conversion %"] = (
    funnel_data["Customers"]
    / funnel_data["Customers"].iloc[0]
    * 100
).round(1)

funnel_data["Drop-Off %"] = (
    100 - funnel_data["Conversion %"]
).round(1)
funnel_fig = px.funnel(
    funnel_data,
    y="Stage",
    x="Customers",
    title="Customer Conversion Funnel"
)

funnel_fig.update_layout(
    template="plotly_white"
)

st.plotly_chart(
    funnel_fig,
    use_container_width=True
)
st.dataframe(
    funnel_data,
    use_container_width=True,
    hide_index=True
)
# =====================================================
# Top Customers by CLTV
# =====================================================

st.markdown("---")
st.subheader("🏆 Top 10 Customers by CLTV")

customer_cltv = (
    filtered
    .groupby("customer_id")["revenue"]
    .sum()
    .reset_index()
    .rename(columns={"revenue": "CLTV"})
    .sort_values(by="CLTV", ascending=False)
)

top_customers = customer_cltv.head(10)
cltv_fig = px.bar(
    top_customers,
    x="CLTV",
    y="customer_id",
    orientation="h",
    title="Top 10 Customers by Lifetime Revenue",
    text_auto=".2s",
    color="CLTV",
    color_continuous_scale="Purples"
)
cltv_fig.update_layout(
    template="plotly_white",
    xaxis_title="Customer Lifetime Value ($)",
    yaxis_title="Customer ID"
)

cltv_fig.update_traces(
    textposition="outside"
)
st.plotly_chart(
    cltv_fig,
    use_container_width=True
)
# =====================================================
# Executive Insights
# =====================================================

st.markdown("---")
st.subheader("📌 Executive Insights")

# Highest Revenue Product
top_product = (
    filtered.groupby("product_name")["revenue"]
    .sum()
    .idxmax()
)

top_product_revenue = (
    filtered.groupby("product_name")["revenue"]
    .sum()
    .max()
)

# Best Partner
top_partner = (
    filtered.groupby("partner_name")["revenue"]
    .sum()
    .idxmax()
)

top_partner_revenue = (
    filtered.groupby("partner_name")["revenue"]
    .sum()
    .max()
)

# Most Adopted Product
most_adopted = (
    filtered.groupby("product_name")["customer_id"]
    .nunique()
    .idxmax()
)

most_adopted_count = (
    filtered.groupby("product_name")["customer_id"]
    .nunique()
    .max()
)

# Highest Funnel Drop-off Stage
funnel_data["Previous"] = funnel_data["Customers"].shift(1)

funnel_data["Drop"] = (
    funnel_data["Previous"] -
    funnel_data["Customers"]
)

largest_drop = funnel_data.loc[
    funnel_data["Drop"].idxmax()
]

drop_stage = largest_drop["Stage"]
drop_count = int(largest_drop["Drop"])

# Insights
st.success(
    f"🏆 Highest Revenue Product: **{top_product}** "
    f"generated **${top_product_revenue:,.2f}** in revenue."
)

st.info(
    f"🤝 Best Performing Partner: **{top_partner}** "
    f"generated **${top_partner_revenue:,.2f}**."
)

st.info(
    f"📦 Most Adopted Product: **{most_adopted}** "
    f"was adopted by **{most_adopted_count}** customers."
)

st.warning(
    f"🎯 Largest Funnel Drop-Off: **{drop_stage}** "
    f"lost **{drop_count}** customers."
)

st.success(
    f"🔄 Cross-Sell Rate: **{cross_sell_rate:.1f}%** of customers "
    f"use more than one financial product."
)

st.success(
    f"🔁 Repeat Usage Rate: **{repeat_rate:.1f}%** of customers "
    f"made more than one transaction."
)