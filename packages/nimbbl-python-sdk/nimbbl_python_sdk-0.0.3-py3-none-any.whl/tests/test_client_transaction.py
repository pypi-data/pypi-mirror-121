import responses
import json

from .helpers import mock_file, ClientTestCase


class TestClientTransaction(ClientTestCase):

    def setUp(self):
        super(TestClientTransaction, self).setUp()

    def test_transaction_fetchall(self):
        res=self.client.transaction.fetch_all("order_Kx7rXXEBqG2bj3q2")
        self.assertEqual(len(res['transactions']),3)


    def test_transaction_fetch(self):
        res=self.client.transaction.fetch_one('order_4JB02okpV922r7yN-20210617102109')
        self.assertEqual(res['transaction_id'],'order_4JB02okpV922r7yN-20210617102109')


    def test_transaction_edit(self):
        self.client.transaction.edit(None)


    def test_transaction_create(self):
        self.client.transaction.create(None)
