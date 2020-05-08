import pandas as pd
import re
import marcformat

class MarcExtractor(object):
    tag_marc_file = 'MARC_FILE'
    tag_filter_columns = 'FILTER_COLUMNS'
    marcFile = ''
    filteredColumns = []
    df = pd.DataFrame()
    df2 = pd.DataFrame()

    def __init__(self, config_file):
        self.__processConfigFile(config_file)
        self.df = pd.read_csv(self.marcFile)
        self.df2 = self.__filterColumns()
        pass

    def __processConfigFile(self, config_file):
        marc_file = re.compile(self.tag_marc_file + '\s*\=\s*')
        filter_columns = re.compile(self.tag_filter_columns + '\s*\=\s*')
        with open(config_file, 'r') as configFile:
            for line in configFile.readlines():
                if re.search(marc_file, line):
                    self.marcFile = line.split('=')[-1].strip()
                elif re.search(filter_columns, line):
                    self.filteredColumns.extend(line.split('=')[-1].replace(' ', '').split(','))
        configFile.close()
        pass

    def __filterColumns(self):
        df = self.df[self.filteredColumns]
        df.columns = [marcformat.marcColumnDirectory[i.zfill(3)] for i in self.filteredColumns]
        df = df[df['ISBN'].notna()]
        df = df[df.ISBN.str.contains('[$]a', regex=True)]
        return df

    def processDataSet(self):
        for column in self.df2:
            if column == "ISBN":
                self.df2[column] = self.df2[column].apply(lambda x: self.__clean_isbn(x))
            elif column == 'Author':
                self.df2[column] = self.df2[column].astype(str).apply(lambda x: self.__clean_author(x))
            elif column == 'Title':
                self.df2[column] = self.df2[column].apply(lambda x: self.__clean_title(x))
            elif column == 'Summary':
                self.df2[column] = self.df2[column].astype(str).apply(lambda x: self.__clean_summary(x))
            elif column == 'Topical_Term':
                self.df2[column] = self.df2[column].astype(str).apply(lambda x: self.__clean_topical_term(x))
            elif column == 'Genre':
                self.df2[column] = self.df2[column].astype(str).apply(lambda x: self.__clean_genre(x))
            else:
                raise Exception('ERROR: Unhandled MARC code!')
        pass

    def getResultDF(self):
        return self.df2

    @staticmethod
    def __lst_to_str(s):
        return "".join(str(i) for i in s)

    def __clean_isbn(self, x):
        regex = r"\ba\w+"
        if re.search(regex, x):
            match = re.search(regex, x)
            result = match.group()
            result = result.replace('a', '')
            return result
        else:
            return x

    def __clean_author(self, x):
        regex1 = r"[$a\s]\w+"
        regex2 = r"[$]a\w+"
        if re.search(regex1, x):
            match = re.findall(regex1, x)
            match = self.__lst_to_str(match)
            match = match.replace(' ', '_')
            match = re.findall(regex2, match)
            match = self.__lst_to_str(match)
            match = match.replace('_', ' ').replace('$a', '')
            return match
        else:
            return x

    def __clean_title(self, x):
        regex1 = r"[$a+-]\w+"
        regex2 = r"[$]a\w+"
        if re.search(regex1, x):
            x = x.replace(' ', '_').replace(',', '_').replace('-', '___').replace('\'', '____')
            match = re.findall(regex1, x)
            match = self.__lst_to_str(match)
            match = re.findall(regex2, match)
            match = self.__lst_to_str(match)
            match = match.replace('____', '\'').replace('___', '-').replace('__', ',_').replace('_', ' ').replace('$a',
                                                                                                                  '')
            return match
        else:
            return x

    def __clean_summary(self, x):
        regex = r"\ba\w+"
        if re.search(regex, x):
            x = x.replace(' ', '_').replace(',', '_').replace('-', '___').replace('.', '____').replace('\'', '_____')
            match = re.search(regex, x)
            result = match.group()
            result = result.replace('a', '', 1).replace('_____', '\'').replace('____', '.').replace('___', '-').replace(
                '__', ',_').replace('_', ' ')
            return result
        else:
            return x

    def __clean_topical_term(self, x):
        x = x.replace(' ', '_')
        regex1 = r"[$]\w+"
        if re.search(regex1, x):
            match = re.findall(regex1, x)
            result = self.__lst_to_str(match).replace('_', ' ')
            return result
        else:
            return x

    def __clean_genre(self, x):
        regex = r"\ba\w+"
        if re.search(regex, x):
            match = re.search(regex, x)
            result = match.group()
            result = result.replace('a', '', 1)
            return result
        else:
            return x


if __name__ == '__main__':
    marcExtractor = MarcExtractor('config.ini')
    marcExtractor.processDataSet()
    df = marcExtractor.getResultDF()
