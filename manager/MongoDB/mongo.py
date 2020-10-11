from pymongo import MongoClient
import re

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
    pyMongoDbClient = None
    errorLog = "./error.log"

    def __init__(self, config_file):
        self.__processConfigFile(config_file)
        self.mongoDBConnectionUri = self.__constructMongoDBConnectionUri(self.mongoDB_ConnectionUri,
                                                                         self.mongoDB_User,
                                                                         self.mongoDB_Password,
                                                                         self.mongoDB_Database)
        pass

    def getMongoDBConnectionUri(self):
        return self.mongoDBConnectionUri

    def __constructMongoDBConnectionUri(self, uri, username, password, db):
        return uri.replace(self.tag_user, username).replace(self.tag_password, password).replace(self.tag_database, db)

    def __processConfigFile(self, config_file):
        mongodb_connection_uri = re.compile('^' + self.tag_mongodb_connection_uri + '\s\=\s')
        mongodb_user = re.compile('^' + self.tag_mongodb_user + '\s*\=\s*')
        mongodb_password = re.compile('^' + self.tag_mongodb_password + '\s*\=\s*')
        mongodb_database = re.compile('^' + self.tag_mongodb_database + '\s*\=\s*')
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
        configFile.close()
        pass

    def pymongoConnectToDB(self):
        self.pyMongoDbClient = MongoClient(self.mongoDBConnectionUri)
        return self.pyMongoDbClient

