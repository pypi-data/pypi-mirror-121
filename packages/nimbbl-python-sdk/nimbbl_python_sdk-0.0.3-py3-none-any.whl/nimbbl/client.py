import os
import json
import requests
import base64
import uuid
# import pkg_resources

# from pkg_resources import DistributionNotFound

from types import ModuleType
from .constants import HTTP_STATUS_CODE, ERROR_CODE, URL

from . import resources, utility

from .errors import (BadRequestError, GatewayError,
                     ServerError)


def capitalize_camel_case(string):
    return "".join(map(str.capitalize, string.split('_')))


# Create a dict of resource classes
RESOURCE_CLASSES = {}
for name, module in resources.__dict__.items():
    if isinstance(module, ModuleType) and \
            capitalize_camel_case(name) in module.__dict__:
        RESOURCE_CLASSES[name] = module.__dict__[capitalize_camel_case(name)]

UTILITY_CLASSES = {}
for name, module in utility.__dict__.items():
    if isinstance(module, ModuleType) and name.capitalize() in module.__dict__:
        UTILITY_CLASSES[name] = module.__dict__[name.capitalize()]


class Client:
    """Nimbbl client class"""

    DEFAULTS = {
        'base_url': URL.BASE_URL
    }

    def __init__(self,access_key=None,secret_key=None, session=None, auth=None, **options):
        """
        Initialize a Client object with session,
        optional auth handler, and options
        """
        self.session = session or requests.Session()
        self.auth = auth
        # file_dir = os.path.dirname(__file__)
        # self.cert_path = file_dir + '/ca-bundle.crt'
        self.bearer=''
        self.basic=''
        self.access_key=access_key
        self.secret=secret_key
        self.isSegmentReq=False
        self.base_url = self._set_base_url(**options)
        self.user_id=''
        self.app_details = []

        # intializes each resource
        # injecting this client object into the constructor
        for name, Klass in RESOURCE_CLASSES.items():
            setattr(self, name, Klass(self))

        for name, Klass in UTILITY_CLASSES.items():
            setattr(self, name, Klass(self))
        self.annonymous_id=self.generate_uiid()
        self.segment_identify()
        if self.bearer=='':
            self.getHeaders(access_key,secret_key)
        

    def _set_base_url(self, **options):
        base_url = self.DEFAULTS['base_url']

        if 'base_url' in options:
            base_url = options['base_url']
            del(options['base_url'])

        return base_url


    def request(self, method, url, **options):
        """
        Dispatches a request to the Nimbbl HTTP API
        """
        response = getattr(self.session, method)(url, 
                                                 **options)
        if ((response.status_code >= HTTP_STATUS_CODE.OK) and
                (response.status_code < HTTP_STATUS_CODE.REDIRECT)):
            return response.json()
        else:
            msg = ""
            code = ""
            json_response = response.json()
            if 'error' in json_response:
                if 'description' in json_response['error']:
                    msg = json_response['error']['description']
                if 'code' in json_response['error']:
                    code = str(json_response['error']['code'])

            if str.upper(code) == ERROR_CODE.BAD_REQUEST_ERROR:
                raise BadRequestError(msg)
            elif str.upper(code) == ERROR_CODE.GATEWAY_ERROR:
                raise GatewayError(msg)
            elif str.upper(code) == ERROR_CODE.SERVER_ERROR:
                raise ServerError(msg)
            else:
                raise ServerError(msg)

    def get(self, path, params, **options):
        """
        Parses GET request options and dispatches a request
        """
        data,options = self._update_request(None, options)
        return self.request('get', path, params=params, **options)

    def post(self, path, data, **options):
        """
        Parses POST request options and dispatches a request
        """
        data, options = self._update_request(data, options)
        return self.request('post', path, data=data, **options)

    def patch(self, path, data, **options):
        """
        Parses PATCH request options and dispatches a request
        """
        data, options = self._update_request(data, options)
        return self.request('patch', path, data=data, **options)

    def delete(self, path, data, **options):
        """
        Parses DELETE request options and dispatches a request
        """
        data, options = self._update_request(data, options)
        return self.request('delete', path, data=data, **options)

    def put(self, path, data, **options):
        """
        Parses PUT request options and dispatches a request
        """
        data, options = self._update_request(data, options)
        return self.request('put', path, data=data, **options)

    def _update_request(self, data, options):
        """
        Updates The resource data and header options
        """
        data = json.dumps(data)
        
        if 'headers' not in options:
            options['headers'] = {}
        headers={'Content-type': 'application/json'}
        if self.isSegmentReq==True:
            headers['Authorization']= 'Basic '+ self.basic
        elif self.bearer != '':
            headers['Authorization']= 'Bearer '+ self.bearer
            if self.nimbbl_key != None and self.nimbbl_key != '':
                headers['x-nimbbl-key']= self.nimbbl_key
        options['headers'].update(headers)
        return data, options
            
    def getHeaders(self,access_key,secret_key):
        self.segment.authReq(access_key)
        data={}
        data[URL.ACCESS_KEY]=access_key
        data[URL.SECRET_KEY]=secret_key
        url = "{}/{}".format(self.base_url,URL.AUTHURL)
        res = self.post(url,data)
        self.segment.authRes(res)
        self.merchent=res["auth_principal"]["sub_merchant_id"]
        self.bearer=res["token"]
        self.nimbbl_key=utility.Utility().generate_nimbbl_header(self.merchent,self.bearer)
        
    def generate_uiid(self):
        return str(uuid.uuid1())
        
    def segment_identify(self):
        segment_bytes = URL.SEGMENT_STRING.encode("ascii")
        base64_bytes=base64.b64encode(segment_bytes)
        base64_string=base64_bytes.decode("ascii")
        self.basic= base64_string
        self.segment.generate_identity_req(self.annonymous_id)