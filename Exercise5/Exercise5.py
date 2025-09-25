import pandas as pd


df = pd.read_csv('../block_15479087.csv')

avg_fee = df["Txn Fee"].mean()
print(f"Average fee: {avg_fee:,.13f}")

# Result: 0.00102482088



