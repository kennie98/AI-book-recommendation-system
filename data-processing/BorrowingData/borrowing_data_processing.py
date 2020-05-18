import pandas as pd

df = pd.read_csv('../Marc/output_marc.csv', dtype=object)
df1 = df.dropna(subset=['ISBN', 'Title'])
df2 = pd.read_csv('./BibUsageWithISBNAvailCopiesByMonth.csv', dtype=object, header=None,
                  names=['BibID', 'ISBN', 'Month', 'Year', 'NumOfAvailItems', 'NumOfCKOs'])
df2 = df2.sort_values(['Year', 'Month'])
df3 = pd.DataFrame.merge(df2, df1, on='ISBN')#, how='left'*/)

df3.to_csv('merged_hpl.csv', index=False)

