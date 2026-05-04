import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Universal Dashboard", layout="wide")

st.title("📊 Universal Data Dashboard")

file = st.file_uploader("Upload CSV", type=["csv"])

if file is not None:
   df = pd.read_csv(file)
   df.columns = df.columns.str.strip()


st.subheader("📄 Data Preview")
st.dataframe(df.head())

# ---- Column Detection ----
numeric_cols = df.select_dtypes(include="number").columns.tolist()
date_cols = df.select_dtypes(include=["datetime", "object"]).columns.tolist()

# ---- User Selection ----
st.sidebar.header("⚙️ Controls")

metric = st.sidebar.selectbox("Select Metric", numeric_cols)

group_col = st.sidebar.selectbox(
    "Group By (Optional)",
    ["None"] + list(df.columns)
)

# Convert date if possible
for col in date_cols:
    try:
        df[col] = pd.to_datetime(df[col])
    except:
        pass

# ---- KPI ----
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total", round(df[metric].sum(), 2))
col2.metric("Average", round(df[metric].mean(), 2))
col3.metric("Max", round(df[metric].max(), 2))

# ---- Trend Chart ----
date_column = None
for col in df.columns:
    if "date" in col.lower():
        date_column = col
        break

if date_column:
    st.subheader("📈 Trend Over Time")
    trend = df.groupby(date_column)[metric].sum().reset_index()
    fig = px.line(trend, x=date_column, y=metric)
    st.plotly_chart(fig, use_container_width=True)

# ---- Grouped Chart ----
if group_col != "None":
    st.subheader(f"📊 {metric} by {group_col}")
    grouped = df.groupby(group_col)[metric].sum().reset_index()
    fig = px.bar(grouped, x=group_col, y=metric)
    st.plotly_chart(fig, use_container_width=True)



