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


if __name__ == '__main__':
    marcQuery = MarcQuery()
    # readers = marcQuery.getGenreRecords('Readers')
    # print(readers)
    # phtographs = marcQuery.getTopicalMainRecords('Photographs')
    # print(phtographs)
    canada = marcQuery.getTopicalGeographicRecords('Canada')
    print(canada)
