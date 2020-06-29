import pandas as pd

df = pd.read_csv('./merged_hpl.csv')
distinctCounter = df.apply(lambda x: len(x.unique()))
print(df.head())