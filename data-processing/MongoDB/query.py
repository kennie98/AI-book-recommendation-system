import mongo as Mongo


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

    def getGenreRecords(self, genre):
        return list(self.marc.find({'Genre': genre}))

    def getTopicalMainRecords(self, topic):
        return list(self.marc.find({'TopicalMain': topic}))

    def getTopicalGeographicRecords(self, topic):
        return list(self.marc.find({'TopicalGeographic': topic}))

    def getAllBookTitles(self):
        return list(self.marc.find({}, {'Title': 1, '_id': 0}))

# get all the book titles and save to file
def getBookTitles(ofile):
    import codecs

    marcQuery = MarcQuery()
    # readers = marcQuery.getGenreRecords('Readers')
    # print(readers)
    # phtographs = marcQuery.getTopicalMainRecords('Photographs')
    # print(phtographs)
    # canada = marcQuery.getTopicalGeographicRecords('Canada')
    # print(canada)
    books = marcQuery.getAllBookTitles()

    bookTitleSet = set()

    with codecs.open(ofile, "w", "utf-8") as Of:
        for book in books:
            bookTitleSet.add(book['Title'].lower())
        for book in bookTitleSet:
            Of.write(book+'\n')
        Of.close()
    return

if __name__ == '__main__':
    # readers = marcQuery.getGenreRecords('Readers')
    # print(readers)
    # phtographs = marcQuery.getTopicalMainRecords('Photographs')
    # print(phtographs)
    # canada = marcQuery.getTopicalGeographicRecords('Canada')
    # print(canada)
    getBookTitles("titleSet.txt")

