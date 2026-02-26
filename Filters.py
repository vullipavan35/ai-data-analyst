import streamlit as st

def apply_filters(df):
    st.sidebar.header("🔎 Filters")

    for column in df.select_dtypes(include=['object']).columns:
        selected = st.sidebar.multiselect(
            f"Filter {column}",
            options=df[column].unique(),
            default=df[column].unique()
        )
        df = df[df[column].isin(selected)]

    return df
