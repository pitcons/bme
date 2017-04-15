from mongoengine import Document, StringField


class Article(Document):
    url = StringField()
    raw = StringField()
    title = StringField()
    bme_version = StringField()            
