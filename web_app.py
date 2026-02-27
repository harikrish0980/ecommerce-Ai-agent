import streamlit as st
import sqlite3
import pandas as pd
from groq import Groq
from dotenv import load_dotenv
import os
import ast

# Load secret key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Connect to database
conn = sqlite3.connect("retail.db")

# Page setup
st.set_page_config(page_title="E-commerce AI Agent", page_icon="🛒", layout="wide")
st.title("🛒 E-commerce Business Intelligence Agent")
st.markdown("Ask any business question about the sales data in plain English.")

def ask_ai_for_sql(user_question):
    prompt = f"""
    You are a SQL expert. I have a table called 'transactions' with these columns:
    - Invoice (order ID)
    - StockCode (product ID)
    - Description (product name)
    - Quantity (units sold)
    - InvoiceDate (date of transaction, format is 'YYYY-MM-DD HH:MM:SS', use STRFTIME for date operations)
    - Price (price per unit)
    - Customer ID (customer number)
    - Country (customer country)
    - Revenue (Quantity x Price)

    Write a single SQLite SQL query to answer this question:
    {user_question}

    Return ONLY the SQL query. No explanation. No markdown. Just the query.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

def run_agent(user_question):
    split_prompt = f"""
    A user asked: "{user_question}"
    
    Split this into one or more separate SQL questions if needed.
    Return ONLY a Python list of strings, one question per item.
    Example: ["What is total revenue?", "Which country is highest?"]
    No explanation. Just the list.
    """
    
    split_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": split_prompt}]
    )
    
    raw = split_response.choices[0].message.content.strip()
    
    try:
        questions = ast.literal_eval(raw)
    except:
        questions = [user_question]
    
    results = []
    for q in questions:
        sql = ask_ai_for_sql(q)
        try:
            df = pd.read_sql(sql, conn)
            results.append({"question": q, "sql": sql, "data": df, "error": None})
        except Exception as e:
            results.append({"question": q, "sql": sql, "data": None, "error": str(e)})
    
    return results

# Sample questions
st.sidebar.header("💡 Sample Questions")
samples = [
    "What are the top 5 countries by revenue?",
    "Which month had the highest sales?",
    "What are the top 10 best selling products?",
    "Who are the top 3 customers by revenue?",
    "How many unique customers do we have?",
    "What is the average order value?",
    "Which day of the week has highest sales?",
]
for s in samples:
    if st.sidebar.button(s):
        st.session_state.question = s

# Question input
question = st.text_input("Your question:", value=st.session_state.get("question", ""))

if st.button("Ask") and question:
    with st.spinner("Thinking..."):
        results = run_agent(question)
    
    for r in results:
        st.subheader(f"📊 {r['question']}")
        if r["error"]:
            st.error(f"Error: {r['error']}")
        else:
            st.dataframe(r["data"], use_container_width=True)
            
            # Auto chart if data has 2 columns and more than 1 row
            df = r["data"]
            if len(df.columns) == 2 and len(df) > 1:
                col1 = df.columns[0]
                col2 = df.columns[1]
                if df[col2].dtype in ["float64", "int64"]:
                    st.bar_chart(df.set_index(col1)[col2])
        with st.expander("See generated SQL"):
            st.code(r["sql"], language="sql")