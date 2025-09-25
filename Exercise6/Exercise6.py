import pandas as pd


df1 = pd.read_csv('../block_15479087.csv')
df2 = pd.read_csv('../block_15479088.csv')


first_50_df1 = df1.iloc[:50]
first_50_df2 = df2.iloc[:50]

combined_df = pd.concat([first_50_df1, first_50_df2], ignore_index=True)

print(f"{combined_df["Txn Fee"].mean(): .10f}")
# Result: 0.0006445939

