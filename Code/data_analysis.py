import pandas as pd

df = pd.read_pickle('Data/Stock/stock_recommendation.pkl')

print(df.info())
print(df)