# -*- coding: utf-8 -*-
import json
from requests import Session
from requests.adapters import HTTPAdapter
from aliyun_core.aliyun_request import AliyunRequest

ALI_SERVER_URL = "https://alidns.cn-hangzhou.aliyuncs.com"
DEFAULT_CONNECTION_TIMEOUT = 15
DEFAULT_POOL_CONNECTIONS = 10
POOL_SIZE = 10

class AliyunClient:
    def __init__(self, access_key_id, access_key_secret):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret

        self.session = Session()
        self.session.mount('https://', HTTPAdapter(DEFAULT_POOL_CONNECTIONS, POOL_SIZE))
        self.session.mount('http://', HTTPAdapter(DEFAULT_POOL_CONNECTIONS, POOL_SIZE))

    def __del__(self):
        if self.session:
            self.session.close()

    def execute(self, request: AliyunRequest):
        if request.method == "POST":
            _url = ALI_SERVER_URL + request.get_url_path(self.access_key_id, self.access_key_secret)
            response = self.session.post(url=_url, timeout=DEFAULT_CONNECTION_TIMEOUT)

            if response.status_code == 200:
                return json.loads(response.text)
            else:
                print("Exception: " + response.text)
        else:
            pass

    def get(self, url, **kwargs):
        return self.session.get( url, **kwargs)
