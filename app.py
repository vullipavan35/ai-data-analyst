from dotenv import load_dotenv
import os
load_dotenv()
# Now the OS can see the key
api_key = os.getenv("OPENAI_API_KEY")

import streamlit as st
import pandas as pd
import plotly.express as px
from langchain_openai import ChatOpenAI
import os

# --- 1. DATA CLEANING ENGINE ---
def clean_data(df):
    # Remove duplicates
    df = df.drop_duplicates()
    # Fill numeric with median, categorical with "Unknown"
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64']:
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna("Unknown")
    return df

# --- 2. SMART AI AGENT (Q&A) ---
def ask_ai(df, question):
    try:
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        # We prompt the LLM to write Python code to answer the question
        prompt = f"""
        You are a data analyst. Dataframe 'df' has columns: {df.columns.tolist()}.
        Question: {question}
        Return ONLY the Python code to solve this. 
        Store the final answer in a variable called 'result'.
        """
        code = llm.invoke(prompt).content.replace("```python", "").replace("```", "")
        
        local_vars = {"df": df}
        exec(code, {}, local_vars)
        return local_vars.get("result", "I couldn't calculate that.")
    except Exception as e:
        return f"Error: {str(e)}"

# --- 3. UI LAYOUT ---
st.set_page_config(page_title="AI Data Dashboard", layout="wide")
st.title("🤖 Automated Data Analyst & Dashboard")

uploaded_file = st.sidebar.file_uploader("Upload your Excel or CSV", type=['csv', 'xlsx'])

if uploaded_file:
    # Load Data
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    df = clean_data(df)
    st.success("✅ Data Uploaded & Cleaned Successfully!")

    # --- TAB 1: Dashboard & KPIs ---
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🔍 Q&A Assistant", "📋 Raw Data"])
    
    with tab1:
        # KPI Row
        cols = st.columns(4)
        num_cols = df.select_dtypes(include='number').columns
        cat_cols = df.select_dtypes(include='object').columns

        cols[0].metric("Total Rows", df.shape[0])
        cols[1].metric("Total Columns", df.shape[1])
        if len(num_cols) > 0:
            cols[2].metric("Numeric Fields", len(num_cols))
            cols[3].metric("Avg Value", f"{df[num_cols[0]].mean():.2f}")

        st.divider()

        # Automatic Charts
        c1, c2 = st.columns(2)
        with c1:
            if len(num_cols) > 0:
                st.subheader("📈 Distribution (Histogram)")
                fig_hist = px.histogram(df, x=num_cols[0], template="plotly_dark", color_discrete_sequence=['#6366f1'])
                st.plotly_chart(fig_hist, use_container_width=True)
        
        with c2:
            if len(cat_cols) > 0 and len(num_cols) > 0:
                st.subheader("🍕 Category Breakdown (Pie)")
                # Grouping top 5 for clarity
                top_5 = df.groupby(cat_cols[0])[num_cols[0]].sum().nlargest(5).reset_index()
                fig_pie = px.pie(top_5, names=cat_cols[0], values=num_cols[0], hole=0.4)
                st.plotly_chart(fig_pie, use_container_width=True)

        if len(cat_cols) > 0 and len(num_cols) > 0:
            st.subheader("🔝 Top 10 Analysis (Bar Chart)")
            top_10 = df.groupby(cat_cols[0])[num_cols[0]].sum().nlargest(10).reset_index()
            fig_bar = px.bar(top_10, x=cat_cols[0], y=num_cols[0], color=num_cols[0])
            st.plotly_chart(fig_bar, use_container_width=True)

    # --- TAB 2: AI Q&A ---
    with tab2:
        st.subheader("💬 Ask anything about your data")
        user_q = st.text_input("Example: What is the total revenue per region?")
        if user_q:
            with st.spinner("Analyzing..."):
                answer = ask_ai(df, user_q)
                st.write("### 💡 Answer:")
                st.info(answer)

    # --- TAB 3: Raw Data ---
    with tab3:
        st.dataframe(df)
