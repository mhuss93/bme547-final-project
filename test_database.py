import pytest
from pymodm.errors import ValidationError


def test_connect():
    import database as db
    from pymodm import MongoModel, fields

    class Test(MongoModel):
        test_id = fields.IntegerField(primary_key=True)
        test_string = fields.CharField()

        class Meta:
            connection_alias = 'bme547-db'

    t = Test(1, test_string='test1')
    t.save()

    out = Test.objects.raw({'_id': 1}).first()
    assert out.test_string == 'test1'


def _test_user(uid):
    import database as db
    db.User(uid).save()


@pytest.mark.parametrize("user_id, filename, extension, image_str", [
    ('1', 'image1', 'gif', 'test_str')
])
def test_upload_image(user_id, filename, extension, image_str):
    import database as db
    import datetime

    _test_user('1')
    time = datetime.datetime.now()
    acceptable_timedelta = datetime.timedelta(seconds=10)
    db.upload_image(user_id, filename, extension, image_str)

    out = db.Image.objects.raw({'_id': user_id+filename+extension}).first()

    pytest.assume(out.filename == filename)
    pytest.assume(out.extension == extension)
    pytest.assume(out.image == image_str)
    pytest.assume(out.user == db.User.objects.raw({'_id': user_id}).first())
    pytest.assume((out.uploadedAt - time) < acceptable_timedelta)


def _del_user(uid):
    import database as db
    try:
        u = db.User.objects.raw({'_id': uid}).first()
    except db.User.DoesNotExist:
        pass
    else:
        u.delete()


def test_register_user():
    import database as db
    import datetime

    _del_user('register_id')
    time = datetime.datetime.now()
    acceptable_timedelta = datetime.timedelta(seconds=10)

    db.register_user('register_id')

    out = db.User.objects.raw({'_id': 'register_id'}).first()
    assert (out.created - time) < acceptable_timedelta


def test_register_user_exception():
    import database as db
    import datetime

    _test_user('exception_id')

    with pytest.raises(db.UserExists):
        db.register_user('exception_id')


def test_get_uploaded_image():
    import database as db

    user_id = 'User1'
    filename = 'test_image1'
    extension = 'tiff'
    image = 'test_str_b64'
    _test_user(user_id)
    db.Image(name=user_id+filename+extension,
             filename=filename,
             extension=extension,
             user=user_id,
             image=image).save()

    out = db.get_uploaded_image(user_id, filename, extension)

    pytest.assume(out['image'] == image)
    pytest.assume(out['extension'] == extension)


def test_save_processed_image():
    import database as db
    import datetime

    _test_user('1')
    time = datetime.datetime.now()
    acceptable_timedelta = datetime.timedelta(seconds=2)
    db.save_processed_image('test_proc1', 'test_proc_str', '1',
                            'HISTOGRAM_EQUALIZATION', time, 1.0)
    out = db.ProcessedImage.objects.raw({'filename': 'test_proc1'}).first()

    pytest.assume(out.timeToProcess == 1.0)
    pytest.assume(out.image == 'test_proc_str')
    pytest.assume(out.processedAt - time < acceptable_timedelta)


def test_save_processed_image_exception():
    import database as db
    import datetime
    time = datetime.datetime.now()

    with pytest.raises(ValidationError):
        db.save_processed_image('test_proc1', 'test_proc_str', '1',
                                'HISTOGRAM_EQUALIZATION', [1.0], '1.0')
