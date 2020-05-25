import datetime
import pandas as pd
from mongoengine import *
import marc
import re


class Mongo:
    tag_mongodb_connection_uri = 'MONGODB_CONNECTION_URI'
    tag_mongodb_user = 'MONGODB_USER'
    tag_mongodb_password = 'MONGODB_PASSWORD'
    tag_mongodb_database = 'MONGODB_DATABASE'
    tag_marc_output_file = 'MARC_OUTPUT_FILE'
    tag_user = '<user>'
    tag_password = '<password>'
    tag_database = '<db>'
    mongoDBConnectionUri = ''
    mongoDBUser = ''
    mongoDBPassword = ''
    mongoDBDatabase = ''
    outputMarcFile = ''
    chunkSize = 1000

    def __init__(self, config_file):
        self.__processConfigFile(config_file)
        self.mongoDBConnectionUri = self.__constructMongoDBConnectionUri(self.mongoDBConnectionUri,
                                                                         self.mongoDBUser,
                                                                         self.mongoDBPassword,
                                                                         self.mongoDBDatabase)
        connect(host=self.mongoDBConnectionUri)
        self.__processMarcOutputFile()
        pass

    def __constructMongoDBConnectionUri(self, uri, username, password, db):
        return uri.replace(self.tag_user, username).replace(self.tag_password, password).replace(self.tag_database, db)

    def __processConfigFile(self, config_file):
        mongodb_connection_uri = re.compile('^' + self.tag_mongodb_connection_uri + '\s\=\s')
        mongodb_user = re.compile('^' + self.tag_mongodb_user + '\s*\=\s*')
        mongodb_password = re.compile('^' + self.tag_mongodb_password + '\s*\=\s*')
        mongodb_database = re.compile('^' + self.tag_mongodb_database + '\s*\=\s*')
        marc_output_file = re.compile('^' + self.tag_marc_output_file + '\s*\=\s*')
        with open(config_file, 'r') as configFile:
            for line in configFile.readlines():
                if re.search(mongodb_connection_uri, line):
                    self.mongoDBConnectionUri = line.split(' = ')[-1].strip()
                elif re.search(mongodb_user, line):
                    self.mongoDBUser = line.split('=')[-1].strip()
                elif re.search(mongodb_password, line):
                    self.mongoDBPassword = line.split('=')[-1].strip()
                elif re.search(mongodb_database, line):
                    self.mongoDBDatabase = line.split('=')[-1].strip()
                elif re.search(marc_output_file, line):
                    self.outputMarcFile = line.split('=')[-1].strip()
        configFile.close()
        pass

    def createMarcDocument(self, bibID, isbn, author, title, summary, genre, topicalMain, topicalGeographic):
        return marc.Marc(
            BibID=bibID,
            ISBN=isbn,
            Author=author,
            Title=title,
            Summary=summary,
            Genre=genre,
            TopicalMain=topicalMain,
            TopicalGeographic=topicalGeographic,
            Stored=DateTimeField(default=datetime.datetime.now))

    def __processMarcOutputFile(self):
        for chunk in pd.read_csv(self.outputMarcFile, chunksize=self.chunkSize, encoding='latin1'):
            df = pd.DataFrame(chunk)
            json = df.to_json(orient='records')



if __name__ == '__main__':
    mongo = Mongo('../config.ini')

# # Establishing a Connection
# connect(
#     host='mongodb+srv://hplDbUser:hplDbUserPassword!@cluster0-n8hpa.gcp.mongodb.net/hpl_db?retryWrites=true&w=majority')
#
#
# # client = pymongo.MongoClient("mongodb+srv://hplDbUser:<password>@cluster0-n8hpa.gcp.mongodb.net/test?retryWrites=true&w=majority")
# # db = client['hpl_db']
# # collection = db['blog_post']
#
# class BlogPost(Document):
#     title = StringField(required=True, max_length=200)
#     posted = DateTimeField(default=datetime.datetime.utcnow)
#     tags = ListField(StringField(max_length=50))
#     meta = {'allow_inheritance': True}
#
#
# class TextPost(BlogPost):
#     content = StringField(required=True)
#
#
# class LinkPost(BlogPost):
#     url = StringField(required=True)
#
#
# # # Defining a Document
# # class Post(Document):
# #     title = StringField(required=True, max_length=200)
# #     content = StringField(required=True)
# #     author = StringField(required=True, max_length=50)
# #     published = DateTimeField(default=datetime.datetime.now)
#
# # Saving Documents
# # post_1 = Post(
# #     title='Sample Post',
# #     content='Some engaging content',
# #     author='Scott'
# # )
# # post_1.save()       # This will perform an insert
# # print(post_1.title)
# # post_1.title = 'A Better Post Title'
# # post_1.save()         # This will perform an atomic edit on "title"
# # print(post_1.title)
# #
# # post_2 = Post(content='Content goes here', author='Michael')
# # post_2.save()
#
# post1 = TextPost(title='Using MongoEngine', content='See the tutorial')
# post1.tags = ['mongodb', 'mongoengine']
# post1.save()
