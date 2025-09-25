import pandas as pd


df = pd.read_csv('../block_15479087.csv')

approved_rows = df[df["Method"] == "Approve"]

print(len(approved_rows))
# Result: 8
