from pymodm import connect, MongoModel, EmbeddedMongoModel, fields

connect('mongodb+srv://mah148:7C2BeZmfwzWmSgwW@bme547-gxtrh.mongodb.net/'
        'test?retryWrites=true', 'bme547-db')


class User(MongoModel):
    userID = fields.CharField(primary_key=True)


class Image(MongoModel):
    name = fields.CharField(primary_key=True)
    filename = fields.CharField()
    extension = fields.CharField()
    image = fields.CharField()
    uploadedAt = fields.DateTimeField()
    user = fields.ReferenceField(User)
