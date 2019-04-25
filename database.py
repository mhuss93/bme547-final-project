from pymodm import connect, MongoModel, EmbeddedMongoModel, fields

connect('mongodb+srv://mah148:7C2BeZmfwzWmSgwW@bme547-gxtrh.mongodb.net/'
        'test?retryWrites=true', 'bme547-db')


class User(MongoModel):
    userID = fields.CharField(primary_key=True)

    class Meta:
        connection_alias = 'bme547-db'


class Image(MongoModel):
    name = fields.CharField(primary_key=True)
    filename = fields.CharField()
    extension = fields.CharField()
    image = fields.CharField()
    uploadedAt = fields.DateTimeField()
    user = fields.ReferenceField(User)

    class Meta:
        connection_alias = 'bme547-db'


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

    class Meta:
        connection_alias = 'bme547-db'


def upload_image(user_id, filename, extension, image_str):
    """Upload a base-64 encoded image to the database.

    :param user_id: Unique User identifier.
    :type user_id: str
    :param filename: Image filename.
    :type filename: str
    :param extension: Image extension.
    :type extension: str
    :param image_str: Base-64 encoded image.
    :type image_str: str
    :return: Job completed message.
    :rtype: str
    """

    from datetime import datetime
    time = datetime.now()
    img = Image(name=user_id+filename+extension,
                filename=filename,
                extension=extension,
                image=image_str,
                uploadedAt=time,
                user=user_id)
    img.save()
    out = "Uploaded {} (userID: {}) at {}.".format(filename, user_id, time)
    return out
