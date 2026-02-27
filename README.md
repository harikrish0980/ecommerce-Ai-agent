# E-commerce AI Agent 🛒

An AI-powered business intelligence tool that lets you query e-commerce sales data using plain English questions.

## What it does
- Ask any business question about sales data in plain English
- AI automatically converts your question into SQL
- Returns results as tables and charts
- Handles multiple questions in one query

## Tech Stack
- Python
- Streamlit (web interface)
- SQLite (database)
- Groq AI / LLaMA 3 (language model)
- Pandas (data processing)

## How to run
1. Clone this repo
2. Install dependencies: `pip install streamlit pandas groq python-dotenv`
3. Add your Groq API key to `.env` file: `GROQ_API_KEY=your_key_here`
4. Add your dataset as `online_retail.csv` in the project folder
5. Run setup: `python setup_db.py`
6. Launch app: `python -m streamlit run app.py`

## Dataset
Uses the UCI Online Retail dataset from Kaggle.
Over 500,000 real e-commerce transactions from a UK retailer.

## Features
- Natural language to SQL conversion
- Auto chart generation
- Multi-question handling
- Sample questions sidebar
