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
