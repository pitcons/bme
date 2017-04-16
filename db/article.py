from mongoengine import Document, StringField, IntField


class Article(Document):
    url = StringField(unique=True)
    raw = StringField()
    title = StringField()
    bme_version = StringField()
    tome = IntField()

    meta = {
        'indexes': [
            'tome',
        ]
    }
