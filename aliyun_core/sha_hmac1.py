# -*- coding: utf-8 -*-
import hashlib
import hmac

from base64 import encodebytes as b64_encode_bytes

def get_sign_string(source, secret):
    source = ensure_bytes(source)
    secret = ensure_bytes(secret)
    h = hmac.new(secret, source, hashlib.sha1)
    signature = ensure_string(b64_encode_bytes(h.digest()).strip())
    return signature

def ensure_bytes(s, encoding='utf-8', errors='strict'):
    if isinstance(s, str):
        return bytes(s, encoding=encoding)
    if isinstance(s, bytes):
        return s
    if isinstance(s, bytearray):
        return bytes(s)
    raise ValueError(
        "Expected str or bytes or bytearray, received %s." %
        type(s))

def ensure_string(s, encoding='utf-8', errors='strict'):
    if isinstance(s, str):
        return s
    if isinstance(s, (bytes, bytearray)):
        return str(s, encoding='utf-8')
    raise ValueError(
        "Expected str or bytes or bytearray, received %s." %
        type(s))
