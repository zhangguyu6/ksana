#-*- coding: utf-8 -*-
import re
from urllib.parse import parse_qs

from httptools import parse_url

from Ksana.cookies import cookiesparser


class Request:
    def __init__(self, ip, url, headers, method, version, keep_alive=None):
        self.ip = ip
        self.query_string = ""
        self.args = {}
        self.rawurl=parse_url(url)
        self.url=self.rawurl.path.decode("utf-8")
        if self.rawurl.query:
            self.query_string = self.rawurl.query.decode("utf-8")
        if self.query_string:
            self.args = parsertodict(self.query_string)

        self.headers={key.decode("utf-8"):value.decode("utf-8") for key,value in  headers.items()}
        self.method=method.decode("utf-8")
        self.version=version
        self.keep_alive=keep_alive
        self.session = None
        self.usersession = None
        self.cookiedict = {}
        self.absurl = "http://" + self.headers['Host'] + self.url + self.query_string
        self._formdata = {}
        if self.headers.get("Cookie"):
            self.cookiedict = cookiesparser(self.headers.get("Cookie"))
        self.body = ""


    def setbody(self,body):
        self.body=body.decode("utf-8")

    @property
    def formdata(self):
        if not self.headers.get("Content-Type"):
            return {}
        if self._formdata or not is_form(self.headers["Content-Type"]):
            return self._formdata
        if "multipart/form-data" in self.headers["Content-Type"]:
            self._formdata = parsermulformdata(self.headers["Content-Type"], self.body)
            return self._formdata
        if "application/x-www-form-urlencoded" in self.headers["Content-Type"]:
            self._formdata = parserurlencodeformdata(self.body)
            return self._formdata
        return {}


def parsertodict(query_string):
    qsdict = parse_qs(query_string)
    if qsdict:
        return {key: value if len(value) > 1 else value[0] for key, value in qsdict.items()}
    else:
        return {key[:-1]: "" for key in query_string.split("&")}


def is_form(contenttype):
    formlist = ["multipart/form-data", "application/x-www-form-urlencoded"]
    for i in formlist:
        if i in contenttype:
            return True
    return False


def parsermulformdata(contenttype, body):
    """
    Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW
    ------WebKitFormBoundary7MA4YWxkTrZu0gW
    Content-Disposition: form-data; name="key1"

    v1
    ------WebKitFormBoundary7MA4YWxkTrZu0gW
    Content-Disposition: form-data; name="key2"

    v2
    -----WebKitFormBoundary7MA4YWxkTrZu0gW--

    """
    boundary = contenttype[contenttype.index("=") + 1:]
    low = body.index(boundary)
    high = body.rindex(boundary)
    formdata = body[low:high].split(boundary)
    formdatadict = {}
    for data in formdata:
        data = data.strip()
        result = re.match(r".*name=\"(?P<name>.*)\"\r\n\r\n(?P<data>.*)", data)
        if result:
            formdatadict[result.groupdict()["name"]] = result.groupdict()["data"]
    return formdatadict


def parserurlencodeformdata(body):
    """
    key-value pair
    """
    if "------WebKitFormBoundary" in body:
        contenttype = "=" + body[:body.index("\r\n")]
        return parsermulformdata(contenttype, body)
    return parsertodict(body)
