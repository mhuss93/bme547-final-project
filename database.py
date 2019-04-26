from pymodm import connect, MongoModel, EmbeddedMongoModel, fields
from pymodm.queryset import QuerySet
from pymodm.manager import Manager

connect('mongodb+srv://mah148:7C2BeZmfwzWmSgwW@bme547-gxtrh.mongodb.net/'
        'test?retryWrites=true', 'bme547-db')


class ImageQuerySet(QuerySet):
    def user(self, user_id):
        '''Return all images uploaded by a User'''
        return self.raw({'user': user_id})

    def userimage(self, user_id, filename, extension):
        '''Return user image indentified by filename and extension.'''
        return self.raw({'user': user_id, 'filename': filename,
                         'extension': extension}).first()


ImageManager = Manager.from_queryset(ImageQuerySet)


class User(MongoModel):
    userID = fields.CharField(primary_key=True)
    created = fields.DateTimeField()

    class Meta:
        connection_alias = 'bme547-db'


class Image(MongoModel):
    name = fields.CharField(primary_key=True)
    filename = fields.CharField()
    extension = fields.CharField()
    image = fields.CharField()
    uploadedAt = fields.DateTimeField()
    user = fields.ReferenceField(User)

    objects = ImageManager()

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


class UserExists(Exception):
    pass


def register_user(user_id):
    """Register a new User on the Database.

    :param user_id: Unique User Identifier.
    :type user_id: str
    :raises UserExists: Exception if User already exists.
    :return: Operation completed string.
    :rtype: str
    """
    u = None
    try:
        u = User.objects.raw({'_id': user_id}).first()
    except User.DoesNotExist:
        pass
    finally:
        if u is not None:
            raise UserExists('User {} exists on the database.'.format(user_id))
        else:
            from datetime import datetime
            time = datetime.now()
            user = User(user_id, created=time)
            user.save()
            out = 'User {} registered.'.format(user_id)
            return out


def get_uploaded_image(user_id, filename, extension):
    """Retrieve an uploaded image.

    :param user_id: Unique User identifier.
    :type user_id: str
    :param filename: Filename.
    :type filename: str
    :param extension: Image extension.
    :type extension: str
    :return: Dictionary of image data.
    :rtype: dict
    """
    img = Image.objects.userimage(user_id, filename, extension)
    img_dict = {
        'image': img.image,
        'extension': img.extension,
        'uploadedAt': img.uploadedAt,
    }
    return img_dict
