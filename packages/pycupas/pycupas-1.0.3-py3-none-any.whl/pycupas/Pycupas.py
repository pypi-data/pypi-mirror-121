import hmac
import hashlib
import os
import requests
import json
from time import gmtime, strftime


class Pycupas:
    def __init__(self,ACCESS_KEY,SECRET_KEY):            
        self.ACCESS_KEY = ACCESS_KEY
        self.SECRET_KEY = SECRET_KEY

    def generateHmac(self,method, url):
        path, *query = url.split('?')
        os.environ['TZ'] = 'GMT+0'
        dt_datetime = strftime('%y%m%d', gmtime()) + 'T' + strftime('%H%M%S', gmtime()) + 'Z'  # GMT+0
        msg = dt_datetime + method + path + (query[0] if query else '')
        signature = hmac.new(bytes(self.SECRET_KEY, 'utf-8'), msg.encode('utf-8'), hashlib.sha256).hexdigest()
    
        return 'CEA algorithm=HmacSHA256, access-key={}, signed-date={}, signature={}'.format(self.ACCESS_KEY, dt_datetime, signature)
    
    def get_cuplink(self,linkList,subId=None):
        REQUEST = dict()
        REQUEST['coupangUrls'] = linkList

        if subId:
            REQUEST['subId'] = subId

        request_method = 'POST'
        domain = 'https://api-gateway.coupang.com'
        api_url = '/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink'    

        authorization = self.generateHmac(request_method, api_url)
        coupang_url = '{}{}'.format(domain, api_url)
        response = requests.request(method=request_method,
                                    url=coupang_url,
                                    headers={'Authorization': authorization, 'Content-Type': 'application/json'},
                                    data=json.dumps(REQUEST),
                                    timeout=20
                                    )
        # 쿠팡 API 호출[IF rCode]
        if (response.json()['rCode'] != '0'):
            print('쿠팡 API 호출 오류[' + str(response.json()['rCode']) + ']')
        
        # 쿠팡 API 호출[result_data]'
        result_data = response.json()['data']
        return result_data         
        

# def cupang_search(categoryId,limit): 
#     # 쿠팡 API 호출[url 설정]
#     subId='shopcollector'
#     request_method = 'GET'
#     domain = 'https://api-gateway.coupang.com'
#     api_url = '/v2/providers/affiliate_open_api/apis/openapi/v1/products/bestcategories/' + str(categoryId) + '?limit=' + str(limit)+'&subId='+str(subId)
    
#     # 쿠팡 API 호출[response]
#     authorization = generateHmac(request_method, api_url, SECRET_KEY, ACCESS_KEY)
#     coupang_url = '{}{}'.format(domain, api_url)
#     response = requests.request(method=request_method,
#                                 url=coupang_url,
#                                 headers={'Authorization': authorization, 'Content-Type': 'application/json'}
#                                 )
    
#     # 쿠팡 API 호출[IF rCode]
#     if (response.json()['rCode'] != '0'):
#         print('쿠팡 API 호출 오류[' + str(response.json()['rCode']) + ']')
    
#     # 쿠팡 API 호출[result_data]'
#     result_data = response.json()['data']
#     return result_data