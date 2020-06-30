import mongo as Mongo

class MarcQuery:
    mongo = None

    def __init__(self):
        self.mongo = Mongo.Mongo('../config.ini')
        self.mongo.connectToMongoDB()

    def getGenreRecords(self, genre):
        return self.mongo.queryMarcDataGenre(genre)

    def getTopicalMainRecords(self, topic):
        return self.mongo.queryMarcDataTopicalMain(topic)

    def getMarcDataTitle(self):
        return self.mongo.getMarcDataTitle()




if __name__ == '__main__':
    marcQuery = MarcQuery()
    marcQuery.getMarcDataTitle()
    readers = marcQuery.getGenreRecords('Readers')
    fiction = marcQuery.getTopicalMainRecords('Fiction')
    sci_fiction = marcQuery.getTopicalMainRecords('Science fiction')
