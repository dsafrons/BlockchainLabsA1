import pandas as pd


df = pd.read_csv('../block_15479087.csv')

df["Value (USD)"] = (
    df["Value (USD)"].astype(str).replace(r"[$,]", "", regex=True).astype(float)
)

idx = df["Value (USD)"].idxmax()
row = df.iloc[idx]

df["Value (USD)"] = (
    df["Value (USD)"].map(lambda x: f"${x:,.2f}").astype(str)
)

print(row)
print("\ntxn hash:", row["Transaction Hash"])

"""
Transaction Hash    0xbac8ee73d816f04798b78bde69f04b969618879a1bf2...
Status                                                        Success
Method                                                       Transfer
Blockno                                                      15479087
DateTime (UTC)                                    2022-09-05 17:21:47
From                       0xa7efae728d2936e78bda97dc267687568dd593f3
From_Nametag                                                    OKX 3
To                         0x332d48a4987d5103e69594ce51cd21d881d02a3f
To_Nametag          Binance Dep: 0x332D48a4987D5103e69594ce51CD21D...
Amount                                                 149.999232 ETH
Value (USD)                                                 620793.53
Txn Fee                                                      0.000651
"""