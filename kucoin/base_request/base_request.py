#!/usr/bin/python
# -*- coding:utf-8 -*-

import json
import aiohttp
import hmac
import hashlib
import base64
import time
from uuid import uuid1
from urllib.parse import urljoin


class KucoinBaseRestApi(object):

    def __init__(self, key='', secret='', passphrase='', is_sandbox=False, url='', is_v1api=False):
        """
        https://docs.kucoin.com

        :param key: Api Token Id  (Mandatory)
        :type key: string
        :param secret: Api Secret  (Mandatory)
        :type secret: string
        :param passphrase: Api Passphrase used to create API  (Mandatory)
        :type passphrase: string
        :param is_sandbox: True sandbox , False  (optional)
        """

        if url:
            self.url = url
        else:
            if is_sandbox:
                self.url = 'https://openapi-sandbox.kucoin.com'
            else:
                self.url = 'https://api.kucoin.com'

        self.session = None # Updated on first `_request`
        self.key = key
        self.secret = secret
        self.passphrase = passphrase
        self.is_v1api = is_v1api

    async def _request(self, method, uri, timeout=10, auth=True, params=None):
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        uri_path = uri
        data_json = ''
        version = 'v1.0.7'
        if method in ['GET', 'DELETE']:
            if params:
                strl = []
                for key in sorted(params):
                    strl.append("{}={}".format(key, params[key]))
                data_json += '&'.join(strl)
                uri += '?' + data_json
                uri_path = uri
        else:
            if params:
                data_json = json.dumps(params)

                uri_path = uri + data_json

        headers = {}
        if auth:
            now_time = int(time.time()) * 1000
            str_to_sign = str(now_time) + method + uri_path
            sign = base64.b64encode(
                hmac.new(self.secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
            if self.is_v1api:
                headers = {
                    "KC-API-SIGN": sign,
                    "KC-API-TIMESTAMP": str(now_time),
                    "KC-API-KEY": self.key,
                    "KC-API-PASSPHRASE": self.passphrase,
                    "Content-Type": "application/json"
                }
            else:
                passphrase = base64.b64encode(
                    hmac.new(self.secret.encode('utf-8'), self.passphrase.encode('utf-8'), hashlib.sha256).digest())
                headers = {
                    "KC-API-SIGN": sign,
                    "KC-API-TIMESTAMP": str(now_time),
                    "KC-API-KEY": self.key,
                    "KC-API-PASSPHRASE": passphrase,
                    "Content-Type": "application/json",
                    "KC-API-KEY-VERSION": "2"
                }
        headers["User-Agent"] = "kucoin-async-python-sdk/"+version
        url = urljoin(self.url, uri)

        if method in ['GET', 'DELETE']:
            async with getattr(self.session, method.lower())(url, headers=headers, timeout=timeout) as response:
                return await self.check_response_data(response)
        else:
            async with getattr(self.session, method.lower())(url, headers=headers, data=data_json, timeout=timeout) as response:
                return await self.check_response_data(response)
    
    async def close(self):
        if not self.session:
            return
        else:
            return await self.session.close()

    @staticmethod
    async def check_response_data(response_data):
        text = await response_data.text()
        if response_data.status == 200:
            try:
                data = json.loads(text)
            except Exception:
                raise Exception(text)
            else:
                if data and data.get('code'):
                    if data.get('code') == '200000':
                        if data.get('data'):
                            return data['data']
                        else:
                            return data
                    else:
                        raise Exception("{}-{}".format(response_data.status, text))
        else:
            raise Exception("{}-{}".format(response_data.status, text))

    @property
    def return_unique_id(self):
        return ''.join([each for each in str(uuid1()).split('-')])
