import pandas as pd


df = pd.read_csv('output_marc.csv')
df1 = df.dropna(subset=['ISBN', 'Title'])
df2 = pd.read_csv('borrow_history.csv', header=None, names=['BibID', 'ISBN', 'Month', 'Year', 'NumOfAvailItems', 'NumOfCKOs'])
df2 = df2.astype('object')
df3 = pd.merge(df1, df2, on='ISBN')


print(df1.dtypes)
print(df2.dtypes)
print(df1.head())
