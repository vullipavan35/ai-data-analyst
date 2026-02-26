import streamlit as st
import pandas as pd
from charts import create_charts
from insights import generate_ai_insights
from kpi import show_kpis
from filters import apply_filters

st.set_page_config(page_title="Excel Data Analyst Agent", layout="wide")

st.title("📊 Excel Data Analyst Agent (Professional Version)")

uploaded_file = st.file_uploader("Upload Excel/CSV File", type=["xlsx", "csv"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    df = apply_filters(df)

    st.subheader("📌 KPI Dashboard")
    show_kpis(df)

    st.subheader("📊 Visual Analytics")
    create_charts(df)

    st.subheader("🤖 AI Insights")
    generate_ai_insights(df)
