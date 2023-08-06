import responses
import json

from .helpers import mock_file, ClientTestCase


class TestClientOrder(ClientTestCase):

    def setUp(self):
        super(TestClientOrder, self).setUp()

    def test_user_fetchall(self):
        res=self.client.user.fetch_all()
        self.assertEqual(len(res['items']),20)


    def test_user_fetch(self):
        res=self.client.user.fetch_one('user_MwvMYXEABm1Oevry')
        self.assertEqual(res['user_id'],'user_MwvMYXEABm1Oevry')


    def test_user_edit(self):
        self.client.user.edit(None)


    def test_user_create(self):
        self.client.user.create(None)
