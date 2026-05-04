import streamlit as st
import pandas as pd

st.set_page_config(page_title="Auto Dashboard", layout="wide")

st.title("Auto Dashboard Generator")

file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

if file is not None:
df = pd.read_csv(file)

```
st.subheader("Dataset Preview")
st.dataframe(df.head())

st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)

numeric_cols = df.select_dtypes(include="number").columns

if len(numeric_cols) >= 1:
    col1.metric("Total", float(df[numeric_cols[0]].sum()))

if len(numeric_cols) >= 2:
    col2.metric("Average", float(df[numeric_cols[1]].mean()))

if len(numeric_cols) >= 3:
    col3.metric("Max", float(df[numeric_cols[2]].max()))

st.subheader("Charts")

if len(numeric_cols) > 0:
    st.line_chart(df[numeric_cols])

cat_cols = df.select_dtypes(include="object").columns

if len(cat_cols) > 0 and len(numeric_cols) > 0:
    grouped = df.groupby(cat_cols[0])[numeric_cols[0]].sum()
    st.bar_chart(grouped)
```
