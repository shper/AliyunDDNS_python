# -*- coding: utf-8 -*-
import aliyun_core.signature_composer as signer

class AliyunRequest:
    def __init__(
            self,
            method,
            action_name,
            version='2015-01-09',
            format="JSON"):
            
            self.method = method
            self._action_name = action_name
            self._version = version
            self._format = format

            self._params = {}
            self._body_params = {}
            self.string_to_sign = ''

    def _get_sign_params(self):
        req_params = self._params
        if req_params is None:
            req_params = {}
        req_params['Version'] = self._version
        req_params['Action'] = self._action_name
        req_params['Format'] = self._format

        return req_params

    def get_url_path(self, access_key_id, access_key_secret):
        sign_params = dict(self._get_sign_params())
        url, string_to_sign = signer.get_signed_url(
            sign_params,
            access_key_id,
            access_key_secret,
            self._format,
            self.method,
            self._body_params)
        self.string_to_sign = string_to_sign
        return url
    
    def put_params(self, key: str, value: str):
        self._params[key] = value
