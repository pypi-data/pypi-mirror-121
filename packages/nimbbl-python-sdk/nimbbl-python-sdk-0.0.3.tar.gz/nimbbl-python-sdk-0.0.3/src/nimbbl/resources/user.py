from .base import Resource
from ..constants.url import URL
from nimbbl.errors import UnsupportedMethodError
import warnings
from .segment import Segment

class User(Resource):
    def __init__(self, client=None):
        super(User, self).__init__(client)
        self.base_url = URL.BASE_URL
        self.segment=Segment()
        self.segment.__init__(client)

    def fetch_all(self, data={}, **kwargs):
        base_url="{}/{}".format(self.base_url,URL.USER_LIST)
        return self.all(base_url,data, **kwargs)

    def fetch_one(self, order_id, data={}, **kwargs):
        base_url="{}/{}".format(self.base_url,URL.USER_GET)
        return self.fetch(base_url,order_id, data, **kwargs)

    def create(self, data={}, **kwargs):
        return UnsupportedMethodError("Unsupported Method")
    
    def edit(self, data={}, **kwargs):
        return UnsupportedMethodError("Unsupported Method")
