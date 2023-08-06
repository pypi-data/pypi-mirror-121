from .base import Resource
from ..constants.url import URL
from nimbbl.errors import UnsupportedMethodError
import warnings
from .segment import Segment
from ..utility import Utility

class Transaction(Resource):
    def __init__(self, client=None):
        super(Transaction, self).__init__(client)
        self.base_url = URL.BASE_URL
        self.segment=Segment()
        self.segment.__init__(client)
        
    def fetch_all(self,order_id, data={}, **kwargs):
        base_url="{}/{}/{}".format(self.base_url,URL.Transaction_LIST,order_id)
        return self.all(base_url,data, **kwargs)

    def fetch_one(self, transaction_id, data={}, **kwargs):
        base_url="{}/{}".format(self.base_url,URL.Transaction_GET)
        self.segment.enquiry_req(transaction_id)
        res= self.fetch(base_url,transaction_id, data, **kwargs)
        self.segment.enquiry_res(res)
        return res


    def create(self, data={}, **kwargs):
        return UnsupportedMethodError("Unsupported Method")
    
    def edit(self, data={}, **kwargs):
        return UnsupportedMethodError("Unsupported Method")

