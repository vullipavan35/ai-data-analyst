import streamlit as st
import pandas as pd
import plotly.express as px
import re

st.set_page_config(page_title="AI Data Analyst", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
.kpi-card {
    background: linear-gradient(135deg,#4f46e5,#06b6d4);
    padding:18px;
    border-radius:12px;
    color:white;
    text-align:center;
    box-shadow:0 2px 8px rgba(0,0,0,0.2);
}
.kpi-card h2 {margin:0;font-size:26px;}
.kpi-card p {margin:0;font-size:13px;opacity:0.9;}
</style>
""", unsafe_allow_html=True)

st.title("AI Data Analyst Dashboard")

uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv","xlsx"])

if uploaded_file:
    # ---------- LOAD ----------
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    num_cols = df.select_dtypes("number").columns.tolist()
    cat_cols = df.select_dtypes("object").columns.tolist()
    date_cols = df.select_dtypes("datetime").columns.tolist()

    # ---------- KPI ROW ----------
    st.markdown("### Overview")

    k1,k2,k3,k4 = st.columns(4)
    k1.markdown(f'<div class="kpi-card"><h2>{df.shape[0]}</h2><p>Rows</p></div>', unsafe_allow_html=True)
    k2.markdown(f'<div class="kpi-card"><h2>{df.shape[1]}</h2><p>Columns</p></div>', unsafe_allow_html=True)
    k3.markdown(f'<div class="kpi-card"><h2>{int(df.isnull().sum().sum())}</h2><p>Missing</p></div>', unsafe_allow_html=True)
    k4.markdown(f'<div class="kpi-card"><h2>{len(num_cols)}</h2><p>Numeric</p></div>', unsafe_allow_html=True)

    st.divider()

    # ---------- MAIN LAYOUT ----------
    left, right = st.columns([1,4])

    # ---------- SLICERS ----------
    with left:
        st.markdown("### Filters")

        selected_cat = None
        if cat_cols:
            selected_cat = st.selectbox("Category", cat_cols)

        selected_num = None
        if num_cols:
            selected_num = st.selectbox("Value", num_cols)

        if date_cols:
            selected_date = st.selectbox("Date", date_cols)
        else:
            selected_date = None

    # ---------- DASHBOARD ----------
    with right:
        r1c1,r1c2 = st.columns(2)

        if selected_cat and selected_num:
            r1c1.plotly_chart(
                px.bar(df, x=selected_cat, y=selected_num, color=selected_cat, title="Category vs Value"),
                use_container_width=True
            )

            r1c2.plotly_chart(
                px.pie(df, names=selected_cat, values=selected_num, title="Distribution"),
                use_container_width=True
            )

        r2c1,r2c2 = st.columns(2)

        if selected_num:
            r2c1.plotly_chart(
                px.histogram(df, x=selected_num, color_discrete_sequence=["#6366f1"], title="Value Distribution"),
                use_container_width=True
            )

        if selected_date and selected_num:
            r2c2.plotly_chart(
                px.line(df, x=selected_date, y=selected_num, title="Trend"),
                use_container_width=True
            )

    st.divider()

    # ---------- QUESTION ----------
    st.markdown("### Ask Questions")

    question = st.text_input("Example: top 5 customers, highest sales")

    if question and selected_cat and selected_num:
        q = question.lower()

        # detect number
        match = re.search(r'\d+', q)
        top_n = int(match.group()) if match else 5

        if "top" in q:
            result = (
                df.groupby(selected_cat)[selected_num]
                .sum()
                .sort_values(ascending=False)
                .head(top_n)
                .reset_index()
            )

            st.success(f"Top {top_n} {selected_cat}")
            st.dataframe(result, use_container_width=True)

        elif "highest" in q or "max" in q:
            idx = df[selected_num].idxmax()
            st.success("Highest Value Record")
            st.dataframe(df.loc[[idx]], use_container_width=True)

        elif "lowest" in q or "min" in q:
            idx = df[selected_num].idxmin()
            st.success("Lowest Value Record")
            st.dataframe(df.loc[[idx]], use_container_width=True)

    st.divider()

    st.markdown("### Data")
    st.dataframe(df, use_container_width=True)
