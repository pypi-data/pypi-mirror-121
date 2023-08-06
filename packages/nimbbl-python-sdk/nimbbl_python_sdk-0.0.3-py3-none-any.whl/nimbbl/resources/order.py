from .segment import Segment
import nimbbl.constants
from os import access, error
from .base import Resource
from ..constants.url import URL
from nimbbl.errors import UnsupportedMethodError
from nimbbl.errors import BadRequestError
import warnings


class Order(Resource):
    def __init__(self, client=None):
        super(Order, self).__init__(client)
        self.base_url = URL.BASE_URL
        self.segment=Segment()
        self.segment.__init__(client)

    
    def fetch_all(self, data={}, **kwargs):
        base_url="{}/{}".format(self.base_url,URL.ORDER_LIST)
        return self.all(base_url,data, **kwargs)

    def fetch_one(self, order_id, data={}, **kwargs):
        base_url="{}/{}".format(self.base_url,URL.ORDER_GET)
        res= self.fetch(base_url,order_id, data, **kwargs)
        if res["message"]=="Order Created Successfully":
            return res
        else:
            raise BadRequestError(res["message"])


    def create(self, data={},**kwargs):
        url="{}/{}".format(self.base_url,URL.ORDER_CREATE)
        self.segment.orderReq(data)
        res = self.post_url(url,data, **kwargs)
        self.segment.orderRes(res)
        return res

    
    def edit(self, data={}, **kwargs):
        return UnsupportedMethodError("Unsupported Method")
