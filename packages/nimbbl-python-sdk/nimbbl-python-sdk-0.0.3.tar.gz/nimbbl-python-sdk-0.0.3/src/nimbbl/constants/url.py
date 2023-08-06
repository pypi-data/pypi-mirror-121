class URL(object):
    BASE_URL = 'https://uatapi.nimbbl.tech/api'
    
    Bearer="Bearer " 
    AUTHURL = "v2/generate-token";
	
    ORDER_CREATE = "v2/create-order";
    ORDER_GET = "v2/get-order";
    ORDER_LIST = "orders/many?f=&pt=yes";
	
    LIST_QUERYPARAM1 = "f";
    LIST_QUERYPARAM2 = "pt";
    NO = "no";
    Empty = "";
	
    USER_CREATE = "users/create";
    USER_GET = "users/one";
    USER_LIST = "users/many?f=&pt=yes";
	
    Transaction_CREATE = "transactions/create";
    Transaction_GET = "v2/fetch-transaction";
    Transaction_LIST = "v2/order/fetch-transactions";
	
    ACCESS_KEY = "access_key";
    SECRET_KEY = "access_secret";
    TOKEN = "token";
    Bearer = "Bearer ";

    SEGMENT = "https://api.segment.io/v1"
    SEGMENT_IDENTIFY = "identify"
    SEGMENT_TRACK = "track"
    SEGMENT_PAGE = "page"
    SEGMENT_SCREEN = "screen"
    SEGMENT_STRING="nvilA20f1bCvxG3GAzYgD43B6gTsdwV9"
    
    AUTH_STATUS="auth_status";
    KIT_NAME="kit_name";
    KIT_VERSION="kit_version";
    INVOICE_ID="invoice_id";
    ORDER_ID= "order_id";
    AMOUNT="amount";
    MERCHANT_ID="merchant_id";
    MERCHANT_NAME="merchant_name";
	
    CONTEXT="context";
    EVENT="event";
    PROPERTIES="properties";
    TIMESTAMP="timestamp";
    PYTHON_SDK = "PYTHON_SDK";
    USER = "userId";
    ORDER_CREATION_REQ = "Order Submitted";
    ORDER_CREATED = "Order Received";
    AUTH_REQ = "Authorization Submitted";
    AUTH_RES = "Authorization Received";
    
    SUCCESS="Success";
    FAILURE="Failure";
    
    ANNONYMOUS_ID="anonymousId";
    TRAITS="traits";
    Enquiry_CREATED="Enquiry Submitted"
    Enquiry_RECIEVED="Enquiry Recieved"
    STATUS="status";
    Transaction_id="Transaction Id";