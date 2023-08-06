import responses
import json
from .testutil import mock_file
from .helpers import mock_file, ClientTestCase


class TestClientOrder(ClientTestCase):

    def setUp(self):
        super(TestClientOrder, self).setUp()

    def test_order_fetchall(self):
        res=self.client.order.fetch_all()
        self.assertEqual(len(res['items']),20)


    def test_order_fetch(self):
        res=self.client.order.fetch_one('order_x1Dve4Ex6KXEm7KB')
        self.assertEqual(res['order_id'],'order_x1Dve4Ex6KXEm7KB')


    def test_order_edit(self):
        self.client.order.edit(None)


    def test_order_create(self):
        req=mock_file("create_order")
        res=self.client.order.create(req)
        self.assertNotEqual(None,res["order_id"])
