import streamlit as st
import pandas as pd
import plotly.express as px
from langchain_openai import ChatOpenAI
import os

# --- 1. SETTINGS & SECRETS ---
st.set_page_config(page_title="AI Data Analyst", layout="wide", page_icon="📊")

# This looks for the key in Streamlit Cloud "Secrets"
api_key = st.secrets.get("OPENAI_API_KEY")

# --- 2. DATA CLEANING ENGINE ---
def clean_data(df):
    df = df.drop_duplicates()
    # Fill numbers with median, text with 'Unknown'
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64']:
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna("Unknown")
    return df

# --- 3. SMART Q&A ENGINE ---
def run_ai_agent(df, question):
    if not api_key or "sk-" not in api_key:
        return "❌ Error: OpenAI API Key is missing or invalid in Streamlit Secrets."
    
    try:
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=api_key)
        
        # We ask the AI to write the Python code to answer the user
        prompt = f"""
        You are a expert Data Analyst. The dataframe is named 'df'.
        Columns: {df.columns.tolist()}
        Question: {question}
        
        Return ONLY valid Python code. 
        Store the final answer in a variable named 'result'. 
        If it's a number, format it nicely.
        """
        
        response = llm.invoke(prompt)
        code = response.content.replace("```python", "").replace("```", "").strip()
        
        # Execute the code safely
        local_vars = {"df": df}
        exec(code, {}, local_vars)
        return local_vars.get("result", "I processed the data but couldn't find a specific result.")
        
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"

# --- 4. USER INTERFACE ---
st.sidebar.title("📂 Data Portal")
if not api_key:
    st.sidebar.error("🔑 API Key Missing in Secrets")
else:
    st.sidebar.success("🔑 API Key Connected")

uploaded_file = st.sidebar.file_uploader("Upload Excel or CSV", type=['csv', 'xlsx'])

if uploaded_file:
    # Load Data
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    df = clean_data(df)
    
    # --- DASHBOARD SECTION ---
    st.title("📊 Automated Data Dashboard")
    
    # KPI Totals
    k1, k2, k3 = st.columns(3)
    k1.metric("Total Records", f"{df.shape[0]:,}")
    k2.metric("Total Columns", df.shape[1])
    
    num_cols = df.select_dtypes(include='number').columns
    cat_cols = df.select_dtypes(include='object').columns
    
    if len(num_cols) > 0:
        k3.metric("Avg Value", f"{df[num_cols[0]].mean():,.2f}")

    st.divider()

    # TABS FOR ORGANIZATION
    tab_dash, tab_qa, tab_raw = st.tabs(["📈 Visuals", "💬 AI Q&A", "📋 Raw Data"])

    with tab_dash:
        col1, col2 = st.columns(2)
        
        with col1:
            if len(num_cols) > 0:
                st.subheader(f"Distribution of {num_cols[0]}")
                fig1 = px.histogram(df, x=num_cols[0], template="plotly_dark")
                st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            if len(cat_cols) > 0 and len(num_cols) > 0:
                st.subheader("Top 5 Categories")
                top5 = df.groupby(cat_cols[0])[num_cols[0]].sum().nlargest(5).reset_index()
                fig2 = px.pie(top5, names=cat_cols[0], values=num_cols[0], hole=0.3)
                st.plotly_chart(fig2, use_container_width=True)

    with tab_qa:
        st.subheader("Ask your data a question")
        user_input = st.text_input("e.g., 'What is the sum of sales for the North region?'")
        if user_input:
            with st.spinner("Thinking..."):
                answer = run_ai_agent(df, user_input)
                st.write("### 💡 AI Answer:")
                st.info(answer)

    with tab_raw:
        st.dataframe(df)

else:
    st.info("👈 Please upload an Excel or CSV file in the sidebar to begin.")
