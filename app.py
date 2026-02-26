import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="AI Data Analyst", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
.kpi {
    background-color:#0E1117;
    padding:20px;
    border-radius:10px;
    text-align:center;
    color:white;
}
.kpi h2 {margin:0;}
.kpi p {margin:0;font-size:14px;color:#9aa0a6;}
</style>
""", unsafe_allow_html=True)

st.title("AI Data Analyst — Premium Dashboard")
st.markdown("Upload CSV or Excel file to generate professional dashboard")

uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv","xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("File uploaded successfully")

    num_cols = df.select_dtypes("number").columns.tolist()
    cat_cols = df.select_dtypes("object").columns.tolist()
    date_cols = df.select_dtypes("datetime").columns.tolist()

    # ---------- FILTERS ----------
    st.markdown("## Filters")

    f1, f2 = st.columns(2)

    if cat_cols:
        category = f1.selectbox("Category Filter", ["All"] + cat_cols)
    else:
        category = None

    if date_cols:
        date_range = f2.date_input("Date Range", [])
    else:
        date_range = None

    filtered_df = df.copy()

    # ---------- KPI ----------
    st.markdown("## Key Metrics")

    k1,k2,k3,k4 = st.columns(4)

    k1.markdown(f'<div class="kpi"><h2>{filtered_df.shape[0]}</h2><p>Rows</p></div>', unsafe_allow_html=True)
    k2.markdown(f'<div class="kpi"><h2>{filtered_df.shape[1]}</h2><p>Columns</p></div>', unsafe_allow_html=True)
    k3.markdown(f'<div class="kpi"><h2>{int(filtered_df.isnull().sum().sum())}</h2><p>Missing</p></div>', unsafe_allow_html=True)
    k4.markdown(f'<div class="kpi"><h2>{len(num_cols)}</h2><p>Numeric</p></div>', unsafe_allow_html=True)

    st.divider()

    # ---------- DASHBOARD ----------
    st.markdown("## Dashboard")

    c1,c2 = st.columns(2)

    if num_cols and cat_cols:
        fig_bar = px.bar(filtered_df, x=cat_cols[0], y=num_cols[0], title="Category vs Value")
        c1.plotly_chart(fig_bar, use_container_width=True)

        fig_pie = px.pie(filtered_df, names=cat_cols[0], values=num_cols[0], title="Distribution")
        c2.plotly_chart(fig_pie, use_container_width=True)

    c3,c4 = st.columns(2)

    if num_cols:
        fig_hist = px.histogram(filtered_df, x=num_cols[0], title="Value Distribution")
        c3.plotly_chart(fig_hist, use_container_width=True)

    if date_cols and num_cols:
        fig_line = px.line(filtered_df, x=date_cols[0], y=num_cols[0], title="Trend Over Time")
        c4.plotly_chart(fig_line, use_container_width=True)

    st.divider()

    # ---------- EXPORT EXCEL ----------
    st.markdown("## Export Dashboard")

    def to_excel(dataframe):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            dataframe.to_excel(writer, index=False, sheet_name='DashboardData')
        return output.getvalue()

    excel_data = to_excel(filtered_df)

    st.download_button(
        label="Download Excel Dashboard",
        data=excel_data,
        file_name="dashboard.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.divider()

    # ---------- DATA ----------
    st.markdown("## Data Preview")
    st.dataframe(filtered_df, use_container_width=True)
    
