import sqlite3
import pandas as pd
from groq import Groq
from dotenv import load_dotenv
import os
import ast

# Load our secret key from .env file
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Connect to database
conn = sqlite3.connect("retail.db")

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
    print(f"\nQuestion: {user_question}")
    
    # Ask AI to split question into separate SQL queries if needed
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
    
    # Parse the list safely
    try:
        questions = ast.literal_eval(raw)
    except:
        questions = [user_question]
    
    # Run each question separately
    for q in questions:
        sql = ask_ai_for_sql(q)
        print(f"\nSub-question: {q}")
        print(f"Generated SQL: {sql}")
        try:
            result = pd.read_sql(sql, conn)
            print(f"Answer:\n{result}")
        except Exception as e:
            print(f"Error running SQL: {e}")

# Interactive chat loop
print("\n=== E-commerce AI Agent ===")
print("Ask any business question about the data. Type 'exit' to quit.\n")

while True:
    question = input("Your question: ")
    if question.lower() == "exit":
        print("Goodbye!")
        break
    run_agent(question)