#
# Pau Freixes, pfreixes@gmail.com
#
# To override with mockable objects, now it needs eve server

import unittest
import eveorm
from eveorm.api import RequestException
from pymongo import MongoClient


class EveOrmTest(unittest.TestCase):
    """
    """
    def setUp(self):
        # test database dependencies for this test suite
        db = MongoClient().test_internet
        db.users.remove()

        self.collection = "users"
        self.eve_rest = "http://localhost:3001/v1"

    def test_get_resources(self):
        api = eveorm.Api(self.eve_rest)
        users = getattr(api.resources, self.collection)

    def test_new_item(self):
        api = eveorm.Api(self.eve_rest)
        users = getattr(api.resources, self.collection)

        # create new item at internet
        item = users.new()
        item.name = "name"
        item.email = "email@gmail.com"
        item.save()

    def test_update_item(self):
        api = eveorm.Api(self.eve_rest)
        users = getattr(api.resources, self.collection)

        item = users.new()
        item.name = "name"
        item.email = "email@gmail.com"
        item.save()

        item = users.get(item.id)
        self.assertEqual(item.name, "name")

        item.name = "modify"
        item.save()

        item = users.get(item.id)
        self.assertEqual(item.name, "modify")

    def test_delete_item(self):
        api = eveorm.Api(self.eve_rest)
        users = getattr(api.resources, self.collection)

        item = users.new()
        item.name = "name"
        item.email = "email@gmail.com"
        item.save()

        item = users.get(item.id)
        item.delete()

        try:
            item = users.get(item.id)
        except RequestException, e:
            self.assertEquals(e.status_code, 404)

    def test_get_all_items(self):
        api = eveorm.Api(self.eve_rest)
        users = getattr(api.resources, self.collection)

        # create 10 new item at internet
        for i in range(0, 10):
            item = users.new()
            item.name = "name"
            item.email = "email@gmail.com"
            item.save()

        l = users.all()
        self.assertEqual(len(l), 10)
