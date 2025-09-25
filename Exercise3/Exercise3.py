import pandas as pd


df1 = pd.read_csv('../block_15479087.csv')
df2 = pd.read_csv('../block_15479088.csv')

last_txn = df1.tail(1)
first_txn = df2.head(1)


average_fee = (last_txn["Txn Fee"].iloc[0] + first_txn["Txn Fee"].iloc[0]) / 2
print(average_fee)
# Result: 0.001227155
