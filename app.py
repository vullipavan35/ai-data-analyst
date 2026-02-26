import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI

# ---------------- AI CLIENT ----------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Data Analyst", layout="wide")

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;color:#4A90E2;'>AI Data Analyst Dashboard</h1>", unsafe_allow_html=True)

# ---------------- FILE UPLOAD ----------------
file = st.file_uploader("Upload CSV or Excel", type=["csv","xlsx"])

if file:
    if file.name.endswith("csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    st.success("Data uploaded successfully")

    # ---------------- SIDEBAR FILTERS ----------------
    st.sidebar.header("Filters")

    for col in df.select_dtypes(include="object").columns:
        unique_vals = df[col].dropna().unique()
        selected = st.sidebar.multiselect(col, unique_vals, default=unique_vals)
        df = df[df[col].isin(selected)]

    # ---------------- KPI DETECTION ----------------
    numeric_cols = df.select_dtypes(include="number").columns

    col1, col2, col3 = st.columns(3)

    if len(numeric_cols) >= 1:
        col1.metric("Total " + numeric_cols[0], int(df[numeric_cols[0]].sum()))

    if len(numeric_cols) >= 2:
        col2.metric("Average " + numeric_cols[1], round(df[numeric_cols[1]].mean(),2))

    col3.metric("Rows", len(df))

    st.divider()

    # ---------------- AUTO CHARTS ----------------
    st.subheader("Visual Insights")

    for num in numeric_cols[:2]:
        for cat in df.select_dtypes(include="object").columns[:1]:
            fig = px.bar(df, x=cat, y=num, color=cat)
            st.plotly_chart(fig, use_container_width=True)

    # ---------------- AI QUESTION BOX ----------------
    st.subheader("Ask Questions About Data")

    question = st.text_input("Example: Top 5 customers by sales")

    if st.button("Get Answer"):
        if question:
            sample = df.head(50).to_csv(index=False)

            prompt = f"""
You are a data analyst.
Dataset sample:
{sample}

Question: {question}

Give concise business answer.
"""

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role":"user","content":prompt}]
            )

            answer = response.choices[0].message.content
            st.success(answer)

else:
    st.info("Upload a dataset to start")
