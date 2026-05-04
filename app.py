import streamlit as st
import pandas as pd

st.set_page_config(page_title="Auto Dashboard", layout="wide")

st.title("📊 Auto Dashboard Generator")

file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

if file:
df = pd.read_csv(file)

```
st.subheader("Dataset Preview")
st.dataframe(df.head())

# KPI Section
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)

numeric_cols = df.select_dtypes(include='number').columns

if len(numeric_cols) >= 1:
    col1.metric("Total", round(df[numeric_cols[0]].sum(), 2))
if len(numeric_cols) >= 2:
    col2.metric("Average", round(df[numeric_cols[1]].mean(), 2))
if len(numeric_cols) >= 3:
    col3.metric("Max", round(df[numeric_cols[2]].max(), 2))

# Charts
st.subheader("Visualizations")

if len(numeric_cols) > 0:
    st.line_chart(df[numeric_cols])

cat_cols = df.select_dtypes(include='object').columns

if len(cat_cols) > 0 and len(numeric_cols) > 0:
    st.bar_chart(df.groupby(cat_cols[0])[numeric_cols[0]].sum())
```
