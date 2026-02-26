import streamlit as st

def generate_ai_insights(df):
    numeric_cols = df.select_dtypes(include=['int64','float64']).columns

    for col in numeric_cols:
        st.write(f"### Insights for {col}")

        st.write(f"- Total: {df[col].sum():,.2f}")
        st.write(f"- Average: {df[col].mean():,.2f}")
        st.write(f"- Max Value: {df[col].max():,.2f}")
        st.write(f"- Min Value: {df[col].min():,.2f}")

        if df[col].iloc[-1] > df[col].mean():
            st.success("Recent values are performing above average.")
        else:
            st.warning("Recent values are below average.")
