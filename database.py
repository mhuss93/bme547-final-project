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


class ProcessedImage(MongoModel):
    filename = fields.CharField()
    image = fields.CharField()
    procedureType = fields.ListField(
        fields.CharField(choices=('HISTOGRAM_EQUALIZATION',
                                  'CONTRAST_STRETCHING',
                                  'LOG_COMPRESSION',
                                  'REVERSE_VIDEO')))
    processedAt = fields.DateTimeField()
    timeToProcess = fields.FloatField()
    user = fields.ReferenceField(User)
    baseImage = fields.ReferenceField(Image)
