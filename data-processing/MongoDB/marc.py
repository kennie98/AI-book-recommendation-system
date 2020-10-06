from mongoengine import *


class Marc(Document):
    BibID = IntField(required=True)
    ISBN = StringField(required=True, max_length=13)
    Author = StringField(max_length=50)
    Title = StringField(required=True, max_length=200)
    Summary = StringField(max_length=3000)
    Genre = StringField(max_length=30)
    TopicalMain = ListField(StringField(max_length=80))
    TopicalGeographic = ListField(StringField(max_length=50))
    meta = {
        'allow_inheritance': True,
        'strict': False,
        'indexes': [
            'ISBN',
            'Genre',
            'TopicalMain'
        ]
    }

    def clean(self):
        """check if title is empty"""
        if self.Title == '':
            msg = 'Draft entries should not have a publication date.'
            raise ValidationError(msg)
