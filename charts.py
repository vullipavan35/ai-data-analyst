import streamlit as st
import plotly.express as px

def create_charts(df):
    numeric_cols = df.select_dtypes(include=['int64','float64']).columns

    if len(numeric_cols) > 0:
        selected_col = st.selectbox("Select Metric", numeric_cols)

        fig1 = px.bar(df, y=selected_col, title="Bar Chart", template="plotly_dark")
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.line(df, y=selected_col, title="Trend Analysis", template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True)

        fig3 = px.histogram(df, x=selected_col, title="Distribution", template="plotly_dark")
        st.plotly_chart(fig3, use_container_width=True)
