# -*- coding: utf-8 -*-
from aliyun_core import *

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
        self._client = AliyunClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET)

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
        _request = AliyunRequest("POST", "DescribeDomainRecords")
        _request.put_params("DomainName", domainName)
        _request.put_params("RRKeyWord", rr)
        _request.put_params("Type", type)

        _response = self._client.execute(_request)
        _result = _response["DomainRecords"]["Record"]
        for record in _result:
            if record["DomainName"] == domainName and record["RR"] == rr and record["Type"] == type:
                return record

    def update_domain_record(self, recordId: str, rr: str, type: str, value:str, line:str = "default"):
        _request = AliyunRequest("POST", "UpdateDomainRecord")
        _request.put_params("RecordId", recordId)
        _request.put_params("RR", rr)
        _request.put_params("Type", type)
        _request.put_params("Value", value)
        _request.put_params("Line", line)
        
        _response = self._client.execute(_request)
        print(_response)

    def get_ip_address(self, url: str) ->str:
        _response = self._client.get(url, timeout=15)
        if _response.status_code == 200:
            return _response.text.strip()
        else:
            raise Exception("The current IP address cannot be obtained. exitting...")

if __name__ == '__main__':
    AliyunDDNS().update_record()
