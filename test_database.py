import pytest


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


def _test_user():
    import database as db
    db.User('1').save()


@pytest.mark.parametrize("user_id, filename, extension, image_str", [
    ('1', 'image1', 'gif', 'test_str')
])
def test_upload_image(user_id, filename, extension, image_str):
    import database as db
    import datetime

    _test_user()
    time = datetime.datetime.now()
    acceptable_timedelta = datetime.timedelta(seconds=10)
    db.upload_image(user_id, filename, extension, image_str)

    out = db.Image.objects.raw({'_id': user_id+filename+extension}).first()

    pytest.assume(out.filename == filename)
    pytest.assume(out.extension == extension)
    pytest.assume(out.image == image_str)
    pytest.assume(out.user == db.User.objects.raw({'_id': user_id}).first())
    pytest.assume((out.uploadedAt - time) < acceptable_timedelta)
