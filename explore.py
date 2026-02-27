import pandas as pd

df = pd.read_csv("online_retail.csv", encoding="latin1")

print("Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())
print("\nBasic info:")
print(df.info())
