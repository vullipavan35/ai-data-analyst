import streamlit as st

def show_kpis(df):
    numeric_cols = df.select_dtypes(include=['int64','float64']).columns

    if len(numeric_cols) >= 1:
        col1, col2, col3 = st.columns(3)

        col = numeric_cols[0]

        with col1:
            st.metric("Total", round(df[col].sum(), 2))

        with col2:
            st.metric("Average", round(df[col].mean(), 2))

        with col3:
            growth = ((df[col].iloc[-1] - df[col].iloc[0]) / df[col].iloc[0]) * 100
            st.metric("Growth %", round(growth, 2))
