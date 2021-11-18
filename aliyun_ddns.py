# -*- coding: utf-8 -*-
import sys
import os

if sys.argv.__len__() > 1 and sys.argv[1] == 'install':
    import pip._internal
else:
    import json
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

MY_IPV4_ECHO_URLS = [
    "https://ipv4.ipw.cn/api/ip/myip", 
    "http://members.3322.org/dyndns/getip",
    "https://v4.ident.me/",
    "http://ip.42.pl/raw",
    "http://ip.3322.net",
    "http://ip.cip.cc"]


class AliyunDDNS:
    def __init__(self):
        self._current_ipv4 = ""
        self._current_ipv6 = ""

        _credential = AccessKeyCredential(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        self._client = AcsClient(region_id='cn-hangzhou', credential=_credential)

    def update_record(self):
        for domian in DOMIANS:
            # Obtain the current IP address.
            if(domian["Type"] == "AAAA"):
                current_ip = self.get_ipv6_address()
            else:
                current_ip = self.get_ipv4_address()
            print("Current ip: " + current_ip)

            if len(current_ip) == 0 or current_ip.isspace() :
                raise Exception("The current IP address cannot be obtained. exitting...")

            record = self.describe_domain_records(domian["DomianName"], domian["RR"], domian["Type"])
            print("Current domain record: " + record.__str__())

            if (record["Value"] != current_ip):
                self.update_domain_record(record["RecordId"], domian["RR"], domian["Type"], current_ip, domian.get("Line", "default"))
            else:
                print("Message: Don't need to update.")
    
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

    def get_ipv4_address(self) -> str:
        if len(self._current_ipv4) == 0 or self._current_ipv4.isspace() :
            for url in MY_IPV4_ECHO_URLS:
                _response = self._client.session.get(url)
                if _response.status_code == 200:
                    self._current_ipv4 = _response.text.strip()
                    return self._current_ipv4
        
        return self._current_ipv4
    
    def get_ipv6_address(self) -> str:
        if len(self._current_ipv6) == 0 or self._current_ipv6.isspace() :
            _process = os.popen("ip addr show | grep 'inet6.*global' | awk '{print $2}' | awk -F'/' '{print $1}' | tail -n 1")
            _output = _process.read()
            self._current_ipv6 = str(_output).strip()
        
        return self._current_ipv6


class Setup:
    @staticmethod
    def install(package: str):
        os.system("python3 -m ensurepip")
        os.system("python3 -m pip install --upgrade pip")
        pip._internal.main(["install", package])


if __name__ == '__main__':
    if sys.argv.__len__() > 1 and sys.argv[1] == 'install':
        Setup.install("aliyun-python-sdk-alidns==2.6.32")
    else:
        AliyunDDNS().update_record()
