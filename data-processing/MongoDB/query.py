import mongo as Mongo
from datetime import datetime
import pymongo
import sys
import zlib, lzma, bz2
import json
import ast


class MarcQuery:
    mongo = None
    client = None
    db = None
    marc = None

    def __init__(self):
        self.mongo = Mongo.Mongo('../config.ini')
        self.client = self.mongo.pymongoConnectToDB()
        self.db = self.client['hpl_db']
        self.marc = self.db['marc']
        # self.marc.create_index([("ISBN", pymongo.ASCENDING)], unique=True)
        # self.marc.create_index([("Title", pymongo.ASCENDING)], unique=True)
        # self.marc.create_index([("Genre", pymongo.ASCENDING)], unique=True)
        # self.marc.create_index([("TopicalMain", pymongo.ASCENDING)], unique=True)
        # self.marc.create_index([("TopicalGeographic", pymongo.ASCENDING)], unique=True)

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
        # titleList = []
        # for g in topicalList:
        #     titleList.extend(self.getTopicalMainRecords(g))
        # return titleList

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


def getBookTitleStringFromAllRecords(bookRecords):
    bookTitles = set()
    for book in bookRecords:
        bookTitles.add(book['Title'].lower())
    bookTitles = list(bookTitles)

    bookTitleString = json.dumps(bookTitles).encode("utf-8")
    # print("before compression: Time =", datetime.now().strftime("%H:%M:%S"))
    # zip_zlib = zlib.compress(bookTitleString)
    # print("zlib finished: Time =", datetime.now().strftime("%H:%M:%S"))
    zip_bz2 = bz2.compress(bookTitleString)
    # print("bz2 finished: Time =", datetime.now().strftime("%H:%M:%S"))
    # zip_lmza = lzma.compress(bookTitleString)
    # print("lmza finished: Time =", datetime.now().strftime("%H:%M:%S"))

    # print('Original data size: ', sys.getsizeof(bookTitleString))
    # print('zlib data size: ', sys.getsizeof(zip_zlib))
    # print('bz2 data size: ', sys.getsizeof(zip_bz2))
    # print('lmza data size: ', sys.getsizeof(zip_lmza))

    # with py7zr.SevenZipFile('titles.7z', 'w') as archive:
    #     archive.writeall('/path/to/base_dir', 'base')

    import codecs
    # bookTitleString = json.dumps(bookTitles)
    with codecs.open("test.bz2", "wb") as Of:
        Of.write(zip_bz2)
    Of.close()
    return json.dumps(bookTitles)


if __name__ == '__main__':
    isbnString = "['9780310714675', '9780763630614', '9781416925330', '9780310714569', '9780152062668', '9781553378907', '9781416915409', '9780142407752', '9780142408094', '9780310714545', '9780310714576', '9781250034366','9780545862615']"

    print("start: Time =", datetime.now().strftime("%H:%M:%S"))

    marcQuery = MarcQuery()
    isbnList = marcQuery.stringToStringList(isbnString)
    recordList = marcQuery.getBookRecordsFromIsbnList(isbnList)

    genreList = marcQuery.getListFromRecords(recordList, "Genre")
    topicalMainList = marcQuery.getListFromRecordLists(recordList, "TopicalMain")
    topicalGeographicList = marcQuery.getListFromRecordLists(recordList, "TopicalGeographic")

    print("Before book record query: Time =", datetime.now().strftime("%H:%M:%S"))

    bookList = marcQuery.getBookRecordsFromGenreAndTopic(genreList, topicalMainList, topicalGeographicList)

    print("After book record query: Time =", datetime.now().strftime("%H:%M:%S"))

    bookListString = getBookTitleStringFromAllRecords(bookList)

    # print(bookListString)
    del marcQuery

    # readers = marcQuery.getGenreRecords('Readers')
    # print(readers)
    # phtographs = marcQuery.getTopicalMainRecords('Photographs')
    # print(phtographs)
    # canada = marcQuery.getTopicalGeographicRecords('Canada')
    # print(canada)
    # getAllBookTitles("titleSet.txt")
