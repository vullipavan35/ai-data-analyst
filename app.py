import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Data Analyst", layout="wide")

st.title("AI Data Analyst & Auto Dashboard Generator")
st.markdown("Upload CSV or Excel file to automatically generate dashboards, KPIs, charts, and insights.")

uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("File uploaded successfully")

    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", int(df.isnull().sum().sum()))
    col4.metric("Numeric Columns", len(df.select_dtypes("number").columns))

    st.divider()

    st.subheader("Auto Dashboard")

    num_cols = df.select_dtypes("number").columns.tolist()
    cat_cols = df.select_dtypes("object").columns.tolist()
    date_cols = df.select_dtypes("datetime").columns.tolist()

    col_left, col_right = st.columns(2)

    if num_cols and cat_cols:
        fig_bar = px.bar(df, x=cat_cols[0], y=num_cols[0], title="Category vs Value")
        col_left.plotly_chart(fig_bar, use_container_width=True)

        fig_pie = px.pie(df, names=cat_cols[0], values=num_cols[0], title="Distribution")
        col_right.plotly_chart(fig_pie, use_container_width=True)

    if num_cols:
        fig_hist = px.histogram(df, x=num_cols[0], title="Value Distribution")
        st.plotly_chart(fig_hist, use_container_width=True)

    if date_cols and num_cols:
        fig_line = px.line(df, x=date_cols[0], y=num_cols[0], title="Trend Over Time")
        st.plotly_chart(fig_line, use_container_width=True)

    st.divider()

    st.subheader("Ask Questions About Your Data")

    question = st.text_input("Type: total, average, max, min")

    if question:
        q = question.lower()

        if "total" in q:
            val = df[num_cols[0]].sum()
            st.success(f"Total {num_cols[0]}: {val:,.2f}")

        elif "average" in q or "mean" in q:
            val = df[num_cols[0]].mean()
            st.success(f"Average {num_cols[0]}: {val:,.2f}")

        elif "max" in q:
            val = df[num_cols[0]].max()
            st.success(f"Max {num_cols[0]}: {val:,.2f}")

        elif "min" in q:
            val = df[num_cols[0]].min()
            st.success(f"Min {num_cols[0]}: {val:,.2f}")

        else:
            st.info("Try: total, average, max, min")

    st.divider()

    st.subheader("Data Preview")
    st.dataframe(df, use_container_width=True)
