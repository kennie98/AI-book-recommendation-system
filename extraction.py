import pandas as pd
import re

#MARC_FILE = 'first_thoudsand_rows.csv'

class Marc_Extractor(object):
  def __init__(self):
      #df = pd.read_csv(marc_file)
      pass

def clean_isbn(x):
    regex = r"\ba\w+"
    if re.search(regex, x):
        match = re.search(regex, x)
        result = match.group()
        result = result.replace('a', '')
        return result
    else:
        return x


def lst_to_str(s):

    str1 = ""

    for ele in s:
        str1 += ele

    return str1


def clean_author(x):
    regex1 = r"[$a\s]\w+"
    regex2 = r"[$]a\w+"
    if re.search(regex1, x):
        match = re.findall(regex1, x)
        match = lst_to_str(match)
        match = match.replace(' ', '_')
        match = re.findall(regex2, match)
        match = lst_to_str(match)
        match = match.replace('_', ' ').replace('$a', '')
        return match
    else:
        return x





if __name__ == '__main__':
    df = pd.read_csv('first_thoudsand_rows.csv')

    df.head()
    df1 = df[['20', '100', '245', '520', '650', '655']]
    df1.columns = ['ISBN', 'Author', 'Title', 'Summary', 'Topical Term', 'Genre']

    df2 = df1[df1['ISBN'].notna()]

    df2 = df2[df2.ISBN.str.contains('[$]a', regex=True)]

    df2['ISBN'] = df2['ISBN'].apply(lambda x: clean_isbn(x))
    df2['Author'] = df2['Author'].astype(str).apply(lambda x: clean_author(x))
    print(df2)



