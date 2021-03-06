import pandas as pd
import numpy as np
import re
import marcformat


class MarcExtractor(object):
    tag_marc_file = 'MARC_FILE'
    tag_filter_columns = 'FILTER_COLUMNS'
    tag_marc_output_file = 'MARC_OUTPUT_FILE'
    marcFile = ''
    marcOutFile = ''
    filteredColumns = []
    df = pd.DataFrame()
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    chunkSize = 1000
    count = 0

    def __init__(self, config_file):
        self.__processConfigFile(config_file)
        pass

    def processDataSet(self):
        header = pd.DataFrame()
        for chunk in pd.read_csv(self.marcFile, chunksize=self.chunkSize, encoding='latin1'):
            if self.count == 0:
                header = [i.zfill(3) for i in chunk.columns]
            chunk.columns = header
            self.count += 1
            print(self.count)
            self.df2 = self.__filterColumns(chunk)
            self.__processColumns()
            self.df2 = self.__filterNone(self.df2)
            self.df2 = self.__nullToNone(self.df2)
            if self.df1.empty:
                self.df1 = self.df2
            else:
                self.df1 = pd.concat([self.df1, self.df2])

    def __processConfigFile(self, config_file):
        marc_file = re.compile('^' + self.tag_marc_file + '\s*\=\s*')
        filter_columns = re.compile('^' + self.tag_filter_columns + '\s*\=\s*')
        marc_out_file = re.compile('^' + self.tag_marc_output_file + '\s*\=\s*')
        with open(config_file, 'r') as configFile:
            for line in configFile.readlines():
                if re.search(marc_file, line):
                    self.marcFile = line.split('=')[-1].strip()
                elif re.search(filter_columns, line):
                    self.filteredColumns.extend(line.split('=')[-1].strip().replace(' ', '').split(','))
                    self.filteredColumns = [i.zfill(3) for i in self.filteredColumns]
                elif re.search(marc_out_file, line):
                    self.marcOutFile = line.split('=')[-1].strip()
        configFile.close()
        pass

    def __filterColumns(self, df):
        df = df[self.filteredColumns]
        df.columns = [marcformat.marcColumnDirectory[i] for i in self.filteredColumns]
        df = self.__filterNaN(df)
        return df

    def __processColumns(self):
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
                self.df2['Topical_Main'] = self.df2[column].astype(str).apply(lambda x: self.__topical_main(x))
                self.df2['Topical_Geographic'] = self.df2[column].astype(str).apply(
                    lambda x: self.__topical_geographic(x))
                self.df2.drop('Topical_Term', axis=1, inplace=True)
            elif column == 'Genre':
                self.df2[column] = self.df2[column].astype(str).apply(lambda x: self.__clean_genre(x))
            elif column == 'BibID':
                self.df2[column] = self.df2[column].apply(str)
            else:
                raise Exception('ERROR: Unhandled MARC code!')
        pass

    def getResultDF(self):
        return self.df1

    def saveToOutFile(self):
        self.df1.to_csv(self.marcOutFile, index=False)

    @staticmethod
    def __lst_to_str(s):
        return "".join(str(i) for i in s)

    @staticmethod
    def __filterNaN(df):
        df.dropna(subset=['ISBN', 'Title'], inplace=True)
        return df

    @staticmethod
    def __nullToNone(df):
        df.where(pd.notnull(df), None)
        return df

    @staticmethod
    def __filterNone(df):
        df['ISBN'].replace(to_replace=[None], value=np.nan, inplace=True)
        df.dropna(subset=['ISBN', 'Title'], inplace=True)
        return df

    def __clean_isbn(self, x):
        regex = r"\ba\w+"
        if re.search(regex, x):
            match = re.search(regex, x)
            result = match.group()
            result = result.replace('a', '')
            result = str(result)
            if result:
                return result

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
        # pattern = r"The maybe house"
        # if x.find(pattern) >= 0:
        #     print("here!")
        if re.search(regex1, x):
            x = x.replace(' ', '_').replace(',', '_').replace('-', '___').replace('\'', '____').replace('\"', '_____')
            match = re.findall(regex1, x)
            match = self.__lst_to_str(match)
            match = re.findall(regex2, match)
            match = self.__lst_to_str(match)
            match = match.replace('_____', '\"').replace('____', '\'').replace('___', '-').replace('__', ',_').replace(
                '_', ' ').replace('$a', '').strip()
            return match
        else:
            return x

    def __clean_summary(self, x):
        regex = r"\ba\w+"
        if re.search(regex, x):
            x = x.replace(' ', '_').replace(',', '_').replace('-', '___').replace('.', '____').replace('\'',
                                                                                                       '_____').replace(
                '\"', '______')
            match = re.search(regex, x)
            if match:
                result = match.group()
                result = result.replace('a', '', 1).replace('______', '\"').replace('_____', '\'').replace('____',
                                                                                                           '.').replace(
                    '___',
                    '-').replace(
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

    def __topical_main(self, x):
        x = x.replace(' ', '_')
        regex1 = r"\b\$v\w+|\$a\w+"
        if re.search(regex1, x):
            match = re.findall(regex1, x)
            result = self.__lst_to_str(match).replace('_', ' ')
            if result.index('$a') == 0:
                result = result.replace('$a', '', 1).replace('$a', ',').replace('$v', ',')
            elif result.index('$v') == 0:
                result = result.replace('$v', '', 1).replace('$a', ',').replace('$a', ',')
            return result

    def __topical_geographic(self, x):
        x = x.replace(' ', '_')
        regex1 = r"[$]z\w+"
        if re.search(regex1, x):
            match = re.findall(regex1, x)
            result = self.__lst_to_str(match).replace('_', ' ')
            if result.index('$z') == 0:
                result = result.replace('$z', '', 1).replace('$z', ',')
            return result

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
    marcExtractor = MarcExtractor('../config.ini')
    marcExtractor.processDataSet()
    marcExtractor.saveToOutFile()
    df = marcExtractor.getResultDF()
    print(df)
