import datetime
from mongoengine import *

class Marc(Document):
    BibID: IntField(required=True)
    ISBN: StringField(required=True, max_length=13)
    Author: StringField(max_length=50)
    Title: StringField(required=True, max_length=200)
    Summary: StringField(max_length=2000)
    Genre: StringField(max_length=30)
    TopicalMain: ListField()
    TopicalGeographic: ListField()
    Stored: DateTimeField(default=datetime.datetime.utcnow)