
from src.eda import calculate_kpis
from src.preprocessing import (
    convert_dates,
    count_missing_values,
    count_duplicate_rows
)
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
from src.insights import (
    get_top_category,
    get_top_region,
    get_top_product,
    get_category_contribution
)

import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="RevenuePulse AI",
    layout="wide"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("RevenuePulse AI Dashboard")

st.markdown("Business Analytics & Sales Intelligence Platform")

# -----------------------------
# FILE UPLOADER
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload Sales CSV File",
    type=["csv"]
)

# -----------------------------
# LOAD DATA
# -----------------------------
if uploaded_file is not None:

    df = pd.read_csv(uploaded_file, encoding="latin1")
    #-----------------------------
    # SIDEBAR FILTERS
    #-----------------------------
    st.sidebar.header("Dashboard Filters")

    selected_regions = st.sidebar.multiselect(
        "Select Region",
        options=df["Region"].unique(),
        default=df["Region"].unique()
    )
    selected_categories = st.sidebar.multiselect(
        "Select Category",
        options=df["Category"].unique(),
        default=df["Category"].unique()
    )
    filtered_df = df[
        (df["Region"].isin(selected_regions))
        &
        (df["Category"].isin(selected_categories))
    ]

    # -----------------------------
    # DATA PREVIEW
    # -----------------------------
    st.subheader("Dataset Preview")
    st.dataframe(df.head())
    # -----------------------------
    # DATA QUALITY CENTER
    # -----------------------------
    st.subheader("Data Quality Report")

    col1, col2, col3, col4 = st.columns(4)

    missing_values = count_missing_values(filtered_df)
    duplicate_rows = count_duplicate_rows(filtered_df)

    col1.metric("Rows", filtered_df.shape[0])
    col2.metric("Columns", filtered_df.shape[1])
    col3.metric("Missing Values", missing_values)
    col4.metric("Duplicate Rows", duplicate_rows)
    missing_df = filtered_df.isnull().sum()
    missing_df = missing_df[missing_df > 0]

    if len(missing_df) > 0:
        st.subheader("Missing Values by Column")
        st.dataframe(missing_df.reset_index())
    else:
        st.success("No missing values found.")

    st.subheader("Column Data Types")

    dtype_df = pd.DataFrame({
        "Column": filtered_df.columns,
        "Data Type": filtered_df.dtypes.astype(str)
    })

    st.dataframe(dtype_df)
    # -----------------------------
    # CLEAN DATE COLUMN
    # -----------------------------
    df = convert_dates(df)

    # -----------------------------
    # KPI SECTION
    # -----------------------------
    st.subheader("Key Performance Indicators")

    kpis = calculate_kpis(filtered_df)

    total_sales = kpis["total_sales"]
    total_profit = kpis["total_profit"]
    total_orders = kpis["total_orders"]
    avg_order_value = kpis["avg_order_value"]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Total Orders", total_orders)
    col4.metric("Avg Order Value", f"${avg_order_value:,.2f}")

    # -----------------------------
    # SALES BY CATEGORY
    # -----------------------------
    st.subheader("Sales by Category")

    category_sales = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig1 = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        color="Category",
        title="Category-wise Sales"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # -----------------------------
    # REGION WISE PROFIT
    # -----------------------------
    st.subheader("Profit by Region")

    region_profit = (
        filtered_df.groupby("Region")["Profit"]
        .sum()
        .reset_index()
    )

    fig2 = px.pie(
        region_profit,
        names="Region",
        values="Profit",
        title="Region-wise Profit Distribution"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # -----------------------------
    # MONTHLY SALES TREND
    # -----------------------------
    st.subheader("Monthly Sales Trend")

    monthly_sales = (
        filtered_df.groupby(
            df["Order Date"].dt.to_period("M")
        )["Sales"]
        .sum()
        .reset_index()
    )

    monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)

    fig3 = px.line(
        monthly_sales,
        x="Order Date",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
    )

    st.plotly_chart(fig3, use_container_width=True)

    # -----------------------------
    # TOP PRODUCTS
    # -----------------------------
    st.subheader("Top 10 Products")

    top_products = (
        filtered_df.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig4 = px.bar(
        top_products,
        x="Sales",
        y="Product Name",
        orientation="h",
        title="Top Selling Products"
    )

    st.plotly_chart(fig4, use_container_width=True)


    # -----------------------------
    # BUSINESS INSIGHTS ENGINE
    # -----------------------------
    st.subheader("Business Insights")

    top_category = get_top_category(filtered_df)

    top_region = get_top_region(filtered_df)

    top_product = get_top_product(filtered_df)

    category_percent = get_category_contribution(filtered_df)

    st.success(
        f"""
        Top Sales Category: {top_category}

        Highest Profit Region: {top_region}

        Best Selling Product: {top_product}

        Leading Category Contribution:
        {category_percent:.2f}% of total sales
        """
    )