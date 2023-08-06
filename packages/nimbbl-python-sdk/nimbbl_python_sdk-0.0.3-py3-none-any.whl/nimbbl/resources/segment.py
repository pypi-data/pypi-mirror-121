from os import access, error
from .base import Resource
from ..constants.url import URL
from nimbbl.errors import UnsupportedMethodError
import warnings
import datetime;
import json

class Segment(Resource):
    def __init__(self, client=None):
        super(Segment, self).__init__(client)
        self.base_url = URL.SEGMENT

   
    def track(self,req, **kwargs):
        self.client.isSegmentReq=True
        url="{}/{}".format(self.base_url,URL.SEGMENT_TRACK)
        res= self.post_url(url, req, **kwargs);
        self.client.isSegmentReq=False
        return res
    
    def identify(self,req, **kwargs):
        self.client.isSegmentReq=True
        url="{}/{}".format(self.base_url,URL.SEGMENT_IDENTIFY)
        res= self.post_url(url, req, **kwargs);
        self.client.isSegmentReq=False
        return res
    
    def page(self,req, **kwargs):
        self.client.isSegmentReq=True
        url="{}/{}".format(self.base_url,URL.SEGMENT_PAGE)
        res= self.post_url(url, req, **kwargs);
        self.client.isSegmentReq=False
        return res
    
    def screen(self,req, **kwargs):
        self.client.isSegmentReq=True
        url="{}/{}".format(self.base_url,URL.SEGMENT_SCREEN)
        res= self.post_url(url, req, **kwargs);
        self.client.isSegmentReq=False
        return res
    
    def authReq(self,access_key):
        jsondata={}
        if self.client.user_id != None and self.client.user_id !='':
            jsondata[URL.USER] = self.client.user_id
        jsondata[URL.ANNONYMOUS_ID]=self.client.annonymous_id
        jsondata[URL.EVENT] = URL.AUTH_REQ
        prop={}
        prop[URL.ACCESS_KEY] = access_key
        prop[URL.KIT_NAME] = URL.PYTHON_SDK
        prop[URL.KIT_VERSION] = "1.0"
        jsondata[URL.PROPERTIES] = prop
        jsondata[URL.TIMESTAMP] = str(datetime.datetime.now())
        return self.track(jsondata)
    
    def authRes(self,res):
        jsondata={}
        if self.client.user_id != None and self.client.user_id !='':
            jsondata[URL.USER] = self.client.user_id
        jsondata[URL.ANNONYMOUS_ID]=self.client.annonymous_id
        jsondata[URL.EVENT] = URL.AUTH_RES
        prop={}
        prop[URL.ACCESS_KEY] = res["auth_principal"]["access_key"]
        prop[URL.AUTH_STATUS] = URL.SUCCESS if (URL.TOKEN in res and 
                                                res[URL.TOKEN] is not None ) else URL.FAILURE
        prop[URL.KIT_NAME] = URL.PYTHON_SDK
        prop[URL.KIT_VERSION] = "1.0"
        jsondata[URL.PROPERTIES] = prop
        jsondata[URL.TIMESTAMP] = str(datetime.datetime.now())
        return self.track(jsondata)
    
    def orderReq(self,jsonReq):
        jsondata={}
        if self.client.user_id != None and self.client.user_id !='':
            jsondata[URL.USER] = self.client.user_id
        jsondata[URL.ANNONYMOUS_ID]=self.client.annonymous_id
        jsondata[URL.EVENT] = URL.ORDER_CREATION_REQ
        prop={}
        prop[URL.KIT_NAME] = URL.PYTHON_SDK
        prop[URL.KIT_VERSION] = "1.0"
        prop[URL.INVOICE_ID]=jsonReq[URL.INVOICE_ID]
        prop[URL.AMOUNT] = jsonReq["total_amount"]
        prop[URL.MERCHANT_ID]= self.client.merchent
        jsondata[URL.PROPERTIES] = prop
        jsondata[URL.TIMESTAMP] = str(datetime.datetime.now())
        return self.track(jsondata)
    
    def orderRes(self,jsonRes):
        jsondata={}
        if self.client.user_id != None and self.client.user_id !='':
            jsondata[URL.USER] = self.client.user_id
        jsondata[URL.ANNONYMOUS_ID]=self.client.annonymous_id
        jsondata[URL.EVENT] = URL.ORDER_CREATED
        prop={}
        prop[URL.KIT_NAME] = URL.PYTHON_SDK
        prop[URL.KIT_VERSION] = "1.0"
        prop[URL.INVOICE_ID]=jsonRes[URL.INVOICE_ID]
        prop[URL.AMOUNT] = jsonRes["total_amount"]
        prop[URL.MERCHANT_ID]= jsonRes["sub_merchant_id"]
        prop[URL.ORDER_ID]= jsonRes[URL.ORDER_ID]
        prop
        jsondata[URL.PROPERTIES] = prop
        jsondata[URL.TIMESTAMP] = str(datetime.datetime.now())
        return self.track(jsondata)
    
    def enquiry_req(self, tranaction_id):
        jsondata={}
        if self.client.user_id != None and self.client.user_id !='':
            jsondata[URL.USER] = self.client.user_id
        jsondata[URL.ANNONYMOUS_ID]=self.client.annonymous_id
        jsondata[URL.EVENT] = URL.Enquiry_CREATED
        prop={}
        prop[URL.KIT_NAME] = URL.PYTHON_SDK
        prop[URL.KIT_VERSION] = "1.0"
        prop[URL.MERCHANT_ID]= self.client.merchent
        prop[URL.Transaction_id]= tranaction_id
        prop
        jsondata[URL.PROPERTIES] = prop
        jsondata[URL.TIMESTAMP] = str(datetime.datetime.now())
        return self.track(jsondata)
    
    def enquiry_res(self, json_Res):
        jsondata={}
        if self.client.user_id != None and self.client.user_id !='':
            jsondata[URL.USER] = self.client.user_id
        jsondata[URL.ANNONYMOUS_ID]=self.client.annonymous_id
        jsondata[URL.EVENT] = URL.Enquiry_RECIEVED
        prop={}
        prop[URL.KIT_NAME] = URL.PYTHON_SDK
        prop[URL.KIT_VERSION] = "1.0"
        prop[URL.MERCHANT_ID]= self.client.merchent
        prop[URL.STATUS]=json_Res["status"]
        prop[URL.Transaction_id]= json_Res["transaction_id"]
        jsondata[URL.PROPERTIES] = prop
        jsondata[URL.TIMESTAMP] = str(datetime.datetime.now())
        return self.track(jsondata)
    
    
    def generate_identity_req(self,annonymous_id):
        jsondata={}
        jsondata[URL.ANNONYMOUS_ID]=annonymous_id
        trait={}
        trait[URL.KIT_NAME] = URL.PYTHON_SDK
        trait[URL.KIT_VERSION] = "1.0"
        jsondata[URL.TRAITS]=trait
        jsondata[URL.TIMESTAMP] = str(datetime.datetime.now())
        return self.identify(jsondata)
    
    