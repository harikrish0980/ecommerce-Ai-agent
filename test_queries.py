import sqlite3
import pandas as pd

# Connect to our database
conn = sqlite3.connect("retail.db")

# Query 1 - Total revenue
query1 = "SELECT ROUND(SUM(Revenue), 2) as Total_Revenue FROM transactions"
result1 = pd.read_sql(query1, conn)
print("Total Revenue:")
print(result1)

# Query 2 - Top 5 countries by revenue
query2 = """
SELECT Country, ROUND(SUM(Revenue), 2) as Revenue
FROM transactions
GROUP BY Country
ORDER BY Revenue DESC
LIMIT 5
"""
result2 = pd.read_sql(query2, conn)
print("\nTop 5 Countries:")
print(result2)

# Query 3 - Top 5 best selling products
query3 = """
SELECT Description, SUM(Quantity) as Units_Sold
FROM transactions
GROUP BY Description
ORDER BY Units_Sold DESC
LIMIT 5
"""
result3 = pd.read_sql(query3, conn)
print("\nTop 5 Products:")
print(result3)

conn.close()