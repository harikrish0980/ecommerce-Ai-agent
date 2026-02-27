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

## Sample Questions & Answers
### Revenue by Country - Table + Auto Chart
![Revenue by Country](screenshot.png)


**Q: What are the top 5 countries by revenue?**
| Country | Revenue |
|---------|---------|
| United Kingdom | 7,308,391 |
| Netherlands | 285,446 |
| EIRE | 265,545 |
| Germany | 228,867 |
| France | 209,042 |

**Q: Which month had the highest sales?**
| Month | Total Sales |
|-------|------------|
| 2011-11 | 1,161,817 |

**Q: Who are the top 3 customers by revenue?**
| Customer ID | Total Revenue |
|-------------|--------------|
| 14646 | 280,206 |
| 18102 | 259,657 |
| 17450 | 194,550 |

##Screenshots
-<img width="1404" height="339" alt="image" src="https://github.com/user-attachments/assets/a7851dad-4232-46c4-a691-9f655c5d0d85" />
-<img width="1472" height="930" alt="image" src="https://github.com/user-attachments/assets/45acbf79-ff43-433b-8b12-4f7b34d51ef5" />
