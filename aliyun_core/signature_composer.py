# -*- coding: utf-8 -*-
import time
import socket
import uuid
from six import iteritems
from six.moves.urllib.parse import urlencode
from six.moves.urllib.request import pathname2url
import aliyun_core.sha_hmac1 as sha_hmac1


def get_timestamp():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def get_uuid():
    name = socket.gethostname() + str(uuid.uuid1())
    namespace = uuid.NAMESPACE_URL
    return str(uuid.uuid5(namespace, name))


def __refresh_sign_parameters(
        parameters,
        access_key_id,
        accept_format="JSON"):
    if parameters is None or not isinstance(parameters, dict):
        parameters = dict()
    if 'Signature' in parameters:
        del parameters['Signature']
    parameters["Timestamp"] = get_timestamp()
    parameters["SignatureMethod"] = "HMAC-SHA1"
    parameters["SignatureType"] = ""
    parameters["SignatureVersion"] = "1.0"
    parameters["SignatureNonce"] = get_uuid()
    parameters["AccessKeyId"] = access_key_id
    if accept_format is not None:
        parameters["Format"] = accept_format
    return parameters


def __pop_standard_urlencode(query):
    ret = query.replace('+', '%20')
    ret = ret.replace('*', '%2A')
    ret = ret.replace('%7E', '~')
    return ret


def __compose_string_to_sign(method, queries):
    sorted_parameters = sorted(iteritems(queries), key=lambda queries: queries[0])
    sorted_query_string = __pop_standard_urlencode(urlencode(sorted_parameters))
    canonicalized_query_string = __pop_standard_urlencode(pathname2url(sorted_query_string))
    string_to_sign = method + "&%2F&" + canonicalized_query_string
    return string_to_sign


def __get_signature(string_to_sign, secret):
    return sha_hmac1.get_sign_string(string_to_sign, secret + '&')


def get_signed_url(params, ak, secret, accept_format, method, body_params):
    url_params = __refresh_sign_parameters(params, ak, accept_format)
    sign_params = dict(url_params)
    sign_params.update(body_params)
    string_to_sign = __compose_string_to_sign(method, sign_params)
    signature = __get_signature(string_to_sign, secret)
    url_params['Signature'] = signature
    url = '/?' + __pop_standard_urlencode(urlencode(url_params))
    return url, string_to_sign