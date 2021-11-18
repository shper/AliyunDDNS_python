# -*- coding: utf-8 -*-
import json
import sys
import pip._internal
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest

# ----- Config Setting -----
ACCESS_KEY_ID = '<your-access-key-id>'
ACCESS_KEY_SECRET = '<your-access-key-secret>'

DOMIANS = [
    {
        "RR": "@",
        "Type": "A",
        "Line": "telecom",
        "DomianName": "shper.cn"
    },
    {
        "RR": "www",
        "Type": "A",
        "Line": "telecom",
        "DomianName": "shper.cn"
    },
    {
        "RR": "@",
        "Type": "AAAA",
        "Line": "telecom",
        "DomianName": "shper.cn"
    },
        {
        "RR": "www",
        "Type": "AAAA",
        "Line": "telecom",
        "DomianName": "shper.cn"
    }
]

MY_IPV6_ECHO_URL = "https://ipv6.ipw.cn/api/ip/myip"
MY_IPV4_ECHO_URL = "https://ipv4.ipw.cn/api/ip/myip"
# MY_IPV4_ECHO_URL = "http://members.3322.org/dyndns/getip"
# MY_IPV4_ECHO_URL = "http://ip.cip.cc"
# MY_IPV4_ECHO_URL = "http://icanhazip.com"

class AliyunDDNS:
    def __init__(self):
        _credential = AccessKeyCredential(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        self._client = AcsClient(region_id='cn-hangzhou', credential=_credential)

    def update_record(self):
        for domian in DOMIANS:
            record = self.describe_domain_records(domian["DomianName"], domian["RR"], domian["Type"])
            print("Current domain record: " + record.__str__())

            # Obtain the current IP address.
            if(domian["Type"] == "AAAA"):
                current_ip = self.get_ip_address(MY_IPV6_ECHO_URL)
            else:
                current_ip = self.get_ip_address(MY_IPV4_ECHO_URL)

            if (record["Value"] != current_ip):
                self.update_domain_record(record["RecordId"], domian["RR"], domian["Type"], current_ip, domian.get("Line", "default"))
            else:
                print("Message: Need not to update, current IP: " + current_ip)
    
    def describe_domain_records(self, domainName: str, rr: str, type: str):
        _request = DescribeDomainRecordsRequest()
        _request.set_accept_format('json')
        _request.set_DomainName(domainName)
        _request.set_RRKeyWord(rr)
        _request.set_Type(type)

        _response = self._client.do_action_with_exception(_request)
        _response = json.loads(str(_response, encoding='utf-8'))

        _records = _response["DomainRecords"]["Record"]
        for record in _records:
            if record["DomainName"] == domainName and record["RR"] == rr and record["Type"] == type:
                return record

    def update_domain_record(self, recordId: str, rr: str, type: str, value: str, line: str = "default"):
        _request = UpdateDomainRecordRequest()
        _request.set_RecordId(recordId)
        _request.set_RR(rr)
        _request.set_Type(type)
        _request.set_Value(value)
        _request.set_Line(line)
        
        _response = self._client.do_action_with_exception(_request)
        print("Result message: " + str(_response, encoding='utf-8'))

    def get_ip_address(self, url: str) ->str:
        _response = self._client.session.get(url, timeout=15)
        if _response.status_code == 200:
            return _response.text.strip()
        else:
            raise Exception("The current IP address cannot be obtained. exitting...")


class Setup:
    @staticmethod
    def install(package: str):
        pip._internal.main(["install", package])


if __name__ == '__main__':
    if sys.argv.__len__() > 1 and sys.argv[1] == 'install':
        Setup.install("aliyun-python-sdk-alidns==2.6.32")
    else:
        AliyunDDNS().update_record()
