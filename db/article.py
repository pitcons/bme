from mongoengine import (Document, StringField, IntField, ListField,
                         MapField, DictField,
                         ReferenceField, ObjectIdField)


class Article(Document):
    url = StringField(unique=True)
    raw = StringField()
    title = StringField(unique=True)
    normalized_title = StringField()
    bme_version = StringField()
    tome = IntField()
    first_sentence = StringField()
    # rutez_path = ListField(StringField)
    # rutez_path = MapField(field=ListField(StringField))
    rutez_path = DictField()
    links = ListField()

    meta = {
        'indexes': [
            'tome',
        ]
    }
