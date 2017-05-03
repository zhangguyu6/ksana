#-*- coding: utf-8 -*-
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
        if self.headers.get("Cookie"):
            self.cookiedict = cookiesparser(self.headers.get("Cookie"))


    def setbody(self,body):
        self.body=body.decode("utf-8")


def parsertodict(query_string):
    return {item.split("=")[0]: item.split("=")[1] or "" for item in query_string.split("&")}
