import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Advanced Dashboard", layout="wide")

st.title("🛒 Supermarket Sales Dashboard")

file = st.file_uploader("Upload CSV", type=["csv"])

if file is not None:
df = pd.read_csv(file)

```
# ---- Data Preparation ----
df.columns = df.columns.str.strip()

# Try to detect common columns
date_col = [col for col in df.columns if "date" in col.lower()]
sales_col = [col for col in df.columns if "sales" in col.lower() or "amount" in col.lower()]
profit_col = [col for col in df.columns if "profit" in col.lower()]
category_col = [col for col in df.columns if "category" in col.lower()]
product_col = [col for col in df.columns if "product" in col.lower()]

if date_col:
    df[date_col[0]] = pd.to_datetime(df[date_col[0]])

# ---- Filters ----
st.sidebar.header("Filters")

if category_col:
    category_filter = st.sidebar.multiselect(
        "Select Category",
        options=df[category_col[0]].unique(),
        default=df[category_col[0]].unique()
    )
    df = df[df[category_col[0]].isin(category_filter)]

# ---- KPI Section ----
st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

if sales_col:
    total_sales = df[sales_col[0]].sum()
    col1.metric("Total Sales", f"{round(total_sales,2)}")

if profit_col:
    total_profit = df[profit_col[0]].sum()
    col2.metric("Total Profit", f"{round(total_profit,2)}")

if sales_col and profit_col:
    margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0
    col3.metric("Profit Margin %", f"{round(margin,2)}%")

col4.metric("Total Records", len(df))

# ---- Sales Trend ----
if date_col and sales_col:
    st.subheader("📈 Sales Trend")
    trend = df.groupby(date_col[0])[sales_col[0]].sum().reset_index()
    fig = px.line(trend, x=date_col[0], y=sales_col[0])
    st.plotly_chart(fig, use_container_width=True)

# ---- Category Analysis ----
if category_col and sales_col:
    st.subheader("📊 Sales by Category")
    cat_data = df.groupby(category_col[0])[sales_col[0]].sum().reset_index()
    fig = px.bar(cat_data, x=category_col[0], y=sales_col[0])
    st.plotly_chart(fig, use_container_width=True)

# ---- Top Products ----
if product_col and sales_col:
    st.subheader("🏆 Top Products")
    top_products = (
        df.groupby(product_col[0])[sales_col[0]]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    fig = px.bar(top_products, x=sales_col[0], y=product_col[0], orientation='h')
    st.plotly_chart(fig, use_container_width=True)

# ---- Raw Data ----
st.subheader("📄 Data Preview")
st.dataframe(df)
```
