from MongoDB.mongo import Mongo
from datetime import datetime
import bz2
import json
import ast
import sys


def log(str):
    print(str, file=sys.stderr)


class MarcQuery:
    mongo = None
    client = None
    db = None
    marc = None

    def __init__(self, path):
        self.mongo = Mongo(path)
        self.client = self.mongo.pymongoConnectToDB()
        self.db = self.client['hpl_db']
        self.marc = self.db['marc']

    def getGenreRecords(self, genre):
        return list(self.marc.find({'Genre': genre}))

    def getTopicalMainRecords(self, topic):
        return list(self.marc.find({'TopicalMain': topic}))

    def getTopicalGeographicRecords(self, topic):
        return list(self.marc.find({'TopicalGeographic': topic}))

    def getIsbnRecords(self, isbn):
        return list(self.marc.find({'ISBN': isbn}))

    def getAllBookTitles(self):
        return list(self.marc.find({}, {'Title': 1, '_id': 0}))

    def getBooksWithGenreList(self, genreList):
        titleList = []
        for g in genreList:
            titleList.extend(self.getGenreRecords(g))
        return titleList

    def getBooksWithTopicalMainList(self, topicalList):
        return list(self.marc.find({'TopicalMain': {'$in': topicalList}}))

    def getBooksWithTopicalGeographicList(self, topicalList):
        titleList = []
        for g in topicalList:
            titleList.extend(self.getTopicalGeographicRecords(g))
        return titleList

    def getBookRecordsFromIsbnList(self, isbnList):
        recordList = []
        for b in isbnList:
            recordList.extend(self.getIsbnRecords(b))
        return recordList

    def getBookRecordsFromGenreAndTopic(self, gList, tmList, tgList):
        return list(self.marc.aggregate([
            {"$match": {
                "$or": [
                    {'Genre': {'$in': gList}},
                    {'TopicalMain': {'$in': tmList}},
                    {'TopicalGeographic': {'$in': tgList}}
                ]
            }},
            {"$project": {
                'ISBN': 1,
                'Title': 1,
                'Author': 1,
            }}
        ]))

    def getRelatedBookRecordsFromBorrowRecords(self, isbnString):
        isbnList = self.stringToStringList(isbnString)
        recordList = self.getBookRecordsFromIsbnList(isbnList)

        genreList = self.getListFromRecords(recordList, "Genre")
        topicalMainList = self.getListFromRecordLists(recordList, "TopicalMain")
        topicalGeographicList = self.getListFromRecordLists(recordList, "TopicalGeographic")

        bookList = self.getBookRecordsFromGenreAndTopic(genreList, topicalMainList, topicalGeographicList)

        log("after book record query: Time ="+datetime.now().strftime("%H:%M:%S"))

        zippedBookListString = self.getZippedBookTitleStringFromAllRecords(bookList)

        return zippedBookListString, bookList

    @staticmethod
    def getListFromRecords(recordList, key):
        valueList = []
        valueList.extend(b[key] for b in recordList)
        valueList = list(set(valueList))
        return valueList

    @staticmethod
    def getListFromRecordLists(recordList, key):
        valueList = []
        for b in recordList:
            valueList.extend(b[key])
        valueList = list(set(valueList))
        return valueList

    @staticmethod
    def getLowerCaseTitlesFromBookRecords(recordList):
        return json.dumps([b['Title'].lower() for b in recordList])

    @staticmethod
    def stringListToString(stringList):
        return json.dumps(stringList)

    @staticmethod
    def stringToStringList(s):
        return ast.literal_eval(s)

    @staticmethod
    def getZippedBookTitleStringFromAllRecords(bookRecords):
        bookTitles = set()
        for book in bookRecords:
            bookTitles.add(book['Title'].lower())
        bookTitles = list(bookTitles)

        bookTitleString = json.dumps(bookTitles).encode("utf-8")
        zip_bz2 = bz2.compress(bookTitleString)
        return zip_bz2

        # import codecs
        # with codecs.open("test.bz2", "wb") as Of:
        #     Of.write(zip_bz2)
        # Of.close()
        # return json.dumps(bookTitles)


# get all the book titles and save to file
def getAllBookTitles(marcQueryObj, ofile):
    import codecs

    books = marcQueryObj.getAllBookTitles()

    bookTitleSet = set()

    with codecs.open(ofile, "w", "utf-8") as Of:
        for book in books:
            bookTitleSet.add(book['Title'].lower())
        for book in bookTitleSet:
            Of.write(book + '\n')
        Of.close()


if __name__ == '__main__':
    # isbnString = "['9780310714675', '9780763630614', '9781416925330', '9780310714569', '9780152062668', '9781553378907', '9781416915409', '9780142407752', '9780142408094', '9780310714545', '9780310714576', '9781250034366','9780545862615']"

    print("start: Time =", datetime.now().strftime("%H:%M:%S"))

    marcQuery = MarcQuery("../config.ini")
    print(marcQuery.getIsbnRecords("0767032357"))
    print(marcQuery.getIsbnRecords("076787708X"))
    print(marcQuery.getIsbnRecords("0788888218"))
    print(marcQuery.getIsbnRecords("076704391X"))
    print(marcQuery.getIsbnRecords("9781627896757"))
    print(marcQuery.getIsbnRecords("0789484250"))
    print(marcQuery.getIsbnRecords("1556706960"))
    print(marcQuery.getIsbnRecords("9780062496775"))
    print(marcQuery.getIsbnRecords("0780676521"))
    print(marcQuery.getIsbnRecords("9780553510584"))
    print(marcQuery.getIsbnRecords("9781616152451"))
    print(marcQuery.getIsbnRecords("9780393082104"))
    print(marcQuery.getIsbnRecords("9781554070398"))
    print(marcQuery.getIsbnRecords("9781610398299"))
    print(marcQuery.getIsbnRecords("1588340090"))
    print(marcQuery.getIsbnRecords("1588171299"))
    print(marcQuery.getIsbnRecords("9781531701956"))
    print(marcQuery.getIsbnRecords("9780736427951"))
    print(marcQuery.getIsbnRecords("079218890X"))
    print(marcQuery.getIsbnRecords("0375421505"))

    print(marcQuery.getIsbnRecords("0767032357"))
    print(marcQuery.getIsbnRecords("9780545565431"))
    print(marcQuery.getIsbnRecords("9781405282130"))
    print(marcQuery.getIsbnRecords("076704391X"))
    print(marcQuery.getIsbnRecords("9780316048699"))
    print(marcQuery.getIsbnRecords("9781497656635"))
    print(marcQuery.getIsbnRecords("9781452128696"))
    print(marcQuery.getIsbnRecords("9781481423199"))
    print(marcQuery.getIsbnRecords("0553801325"))
    print(marcQuery.getIsbnRecords("9781606844199"))
    print(marcQuery.getIsbnRecords("9780698197268"))
    print(marcQuery.getIsbnRecords("9781627896757"))
    print(marcQuery.getIsbnRecords("9780062183804"))
    print(marcQuery.getIsbnRecords("9781927668412"))
    print(marcQuery.getIsbnRecords("9780545528436"))
    print(marcQuery.getIsbnRecords("9781503825314"))
    print(marcQuery.getIsbnRecords("9780544313514"))
    print(marcQuery.getIsbnRecords("9781460255933"))
    print(marcQuery.getIsbnRecords("9781452400303"))
    print(marcQuery.getIsbnRecords("9781582703923"))
    # bookListString, bookList = marcQuery.getRelatedBookRecordsFromBorrowRecords(isbnString)

    del marcQuery

    # readers = marcQuery.getGenreRecords('Readers')
    # print(readers)
    # phtographs = marcQuery.getTopicalMainRecords('Photographs')
    # print(phtographs)
    # canada = marcQuery.getTopicalGeographicRecords('Canada')
    # print(canada)
    # getAllBookTitles("titleSet.txt")
