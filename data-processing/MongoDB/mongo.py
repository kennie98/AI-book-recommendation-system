import datetime
import pandas as pd
from mongoengine import *
import re


class Marc(Document):
    BibID = IntField(required=True)
    ISBN = StringField(required=True, max_length=13)
    Author = StringField(max_length=50)
    Title = StringField(required=True, max_length=200)
    Summary = StringField(max_length=2000)
    Genre = StringField(max_length=30)
    TopicalMain = ListField(StringField(max_length=80))
    TopicalGeographic = ListField(StringField(max_length=50))
    meta = {'allow_inheritance': True, 'strict': False}


class NewDoc(Marc):
    Stored = DateTimeField(default=datetime.datetime.utcnow)
    meta = {'strict': False}


class Mongo:
    tag_mongodb_connection_uri = 'MONGODB_CONNECTION_URI'
    tag_mongodb_user = 'MONGODB_USER'
    tag_mongodb_password = 'MONGODB_PASSWORD'
    tag_mongodb_database = 'MONGODB_DATABASE'
    tag_mongodb_collection = 'MONGODB_COLLECTION'
    tag_marc_output_file = 'MARC_OUTPUT_FILE'
    tag_user = '<user>'
    tag_password = '<password>'
    tag_database = '<db>'
    mongoDB_ConnectionUri = ''
    mongoDB_User = ''
    mongoDB_Password = ''
    mongoDB_Database = ''
    mongoDB_Collection = ''
    outputMarcFile = ''
    chunkSize = 1000
    bookList = []
    mongoDBClient = None
    mongoDBDatabase = None
    mongoDBCollection = None

    def __init__(self, config_file):
        self.__processConfigFile(config_file)
        self.mongoDBConnectionUri = self.__constructMongoDBConnectionUri(self.mongoDB_ConnectionUri,
                                                                         self.mongoDB_User,
                                                                         self.mongoDB_Password,
                                                                         self.mongoDB_Database)
        pass

    def __constructMongoDBConnectionUri(self, uri, username, password, db):
        return uri.replace(self.tag_user, username).replace(self.tag_password, password).replace(self.tag_database, db)

    def __processConfigFile(self, config_file):
        mongodb_connection_uri = re.compile('^' + self.tag_mongodb_connection_uri + '\s\=\s')
        mongodb_user = re.compile('^' + self.tag_mongodb_user + '\s*\=\s*')
        mongodb_password = re.compile('^' + self.tag_mongodb_password + '\s*\=\s*')
        mongodb_database = re.compile('^' + self.tag_mongodb_database + '\s*\=\s*')
        mongodb_collection = re.compile('^' + self.tag_mongodb_collection + '\s*\=\s*')
        marc_output_file = re.compile('^' + self.tag_marc_output_file + '\s*\=\s*')
        with open(config_file, 'r') as configFile:
            for line in configFile.readlines():
                if re.search(mongodb_connection_uri, line):
                    self.mongoDB_ConnectionUri = line.split(' = ')[-1].strip()
                elif re.search(mongodb_user, line):
                    self.mongoDB_User = line.split('=')[-1].strip()
                elif re.search(mongodb_password, line):
                    self.mongoDB_Password = line.split('=')[-1].strip()
                elif re.search(mongodb_database, line):
                    self.mongoDB_Database = line.split('=')[-1].strip()
                elif re.search(marc_output_file, line):
                    self.outputMarcFile = line.split('=')[-1].strip()
                elif re.search(mongodb_collection, line):
                    self.mongoDB_Collection = line.split('=')[-1].strip()
        configFile.close()
        pass

    @staticmethod
    def __convertStringToList(s):  # convert a string of items separated by comma, and get rid of duplicates
        return list(set(s.split(',')))

    def processMarcOutputFile(self):
        self.bookList = []
        count = 0
        for chunk in pd.read_csv(self.outputMarcFile, chunksize=self.chunkSize, encoding='latin1'):
            count += 1
            print(count)
            df = pd.DataFrame(chunk)
            j = [{**row.dropna().to_dict()} for index, row in df.iterrows()]

            for i in j:
                if "Topical_Main" in i:
                    i['Topical_Main'] = self.__convertStringToList(i['Topical_Main'])
                if "Topical_Geographic" in i:
                    i['Topical_Geographic'] = self.__convertStringToList(i['Topical_Geographic'])
                self.bookList.append(i)

    def __createMarcRecord(self, rec):
        return NewDoc(
            BibID=rec['BibID'],
            ISBN=rec['ISBN'],
            Title=rec['Title'],
            Author=rec['Author'] if "Author" in rec else None,
            Summary=rec['Summary'] if "Summary" in rec else None,
            Genre=rec['Genre'] if "Genre" in rec else None,
            TopicalMain=rec['Topical_Main'] if "Topical_Main" in rec else None,
            TopicalGeographic=rec['Topical_Geographic'] if "Topical_Geographic" in rec else None,
            Stored=datetime.datetime.now()
        )

    def connectToMongoDB(self):
        self.mongoDBClient = connect(host=self.mongoDBConnectionUri)
        self.mongoDBDatabase = self.mongoDBClient[self.mongoDB_Database]
        self.mongoDBCollection = self.mongoDBDatabase[self.mongoDB_Collection]

    def storeToMongoDB(self):
        count = 0
        for i in self.bookList:
            count += 1
            print(count)
            marcRec = self.__createMarcRecord(i)
            marcRec.save()


if __name__ == '__main__':
    mongo = Mongo('../config.ini')
    mongo.processMarcOutputFile()

    print("=================== store to MongoDB ===================")
    mongo.connectToMongoDB()
    mongo.storeToMongoDB()
    print("=================== DONE ===================")