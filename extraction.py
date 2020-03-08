import pandas as pd
import re

#MARC_FILE = 'first_thoudsand_rows.csv'

class Marc_Extractor(object):
  def __init__(self):
      #df = pd.read_csv(marc_file)
      pass



if __name__ == '__main__':
    df = pd.read_csv('first_thoudsand_rows.csv')

    df.head()
    df1 = df[['20', '100', '245', '520', '650', '655']]
    df1.columns = ['ISBN', 'Author', 'Title', 'Summary', 'Topical Term', 'Genre']
    #df['20'].values
    df2 = df1['ISBN']
    #print(df2)
    #x = re.search("^$a.*;$", txt)
    txt = "\\\\$a0802019862$(pa.:)$c3.95"

    x = re.search(r"\ba\w+", txt)
    print(x)
    print("string is ", x.group())

