import pandas as pd

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
    print(df1)