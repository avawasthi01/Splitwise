from mongoengine import Document, StringField


class User(Document):
    name = StringField(required=True, max_length=50)
    email = StringField(required=True, unique=True, max_length=100)
    mobile_number = StringField(required=True, max_length=15)
