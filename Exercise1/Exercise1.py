import pandas as pd


block_data = pd.read_csv('../block_15479087.csv')

df_fees = block_data[['Transaction Hash', 'Txn Fee']]

target_tx_start = "0x84ae"
tx_idx = None

for tx in block_data["Transaction Hash"]:
    idx = block_data[block_data['Transaction Hash'] == tx].index
    if target_tx_start in tx[:len(target_tx_start)]:
        tx_idx = idx

if tx_idx is None:
    raise Exception("No transaction found")

tx_idx = tx_idx.values[0]

tx0 = df_fees.iloc[tx_idx - 1]
tx1 = df_fees.iloc[tx_idx]
tx2 = df_fees.iloc[tx_idx + 1]

txs_fees = [tx0["Txn Fee"], tx1["Txn Fee"], tx2["Txn Fee"]]
average_fee = sum(txs_fees) / len(txs_fees)

print(average_fee)
# Result: 0.00172267


