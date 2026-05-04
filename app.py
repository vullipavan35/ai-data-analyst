import streamlit as st
import pandas as pd

st.set_page_config(page_title="Auto Dashboard", layout="wide")

st.title("📊 Auto Dashboard Generator")

file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

if file is not None:
df = pd.read_csv(file)

```
st.subheader("Dataset Preview")
st.dataframe(df.head())

numeric_cols = df.select_dtypes(include='number').columns
cat_cols = df.select_dtypes(include='object').columns

st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)

if len(numeric_cols) >= 1:
    col1.metric("Total", round(df[numeric_cols[0]].sum(), 2))

if len(numeric_cols) >= 2:
    col2.metric("Average", round(df[numeric_cols[1]].mean(), 2))

if len(numeric_cols) >= 3:
    col3.metric("Maximum", round(df[numeric_cols[2]].max(), 2))

st.subheader("Line Chart")

if len(numeric_cols) > 0:
    st.line_chart(df[numeric_cols])

st.subheader("Bar Chart")

if len(cat_cols) > 0 and len(numeric_cols) > 0:
    chart_data = df.groupby(cat_cols[0])[numeric_cols[0]].sum()
    st.bar_chart(chart_data)
```

else:
st.info("Please upload a CSV file to generate dashboard.")
