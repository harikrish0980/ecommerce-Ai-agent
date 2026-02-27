import pandas as pd
import sqlite3

# Load data
df = pd.read_csv("online_retail.csv", encoding="latin1")

# Clean data
df = df.dropna(subset=["Customer ID"])
df = df[df["Quantity"] > 0]
df = df[df["Price"] > 0]

# Add revenue column
df["Revenue"] = df["Quantity"] * df["Price"]

# Fix date format to proper SQLite format
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"]).dt.strftime('%Y-%m-%d %H:%M:%S')

# Save to a local database
conn = sqlite3.connect("retail.db")
df.to_sql("transactions", conn, if_exists="replace", index=False)
conn.close()

print("Done! Database created.")
print(f"Clean rows: {len(df)}")