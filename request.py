#-*- coding: utf-8 -*-
from httptools import parse_url
class Request:
    def __init__(self,url,headers,method,version,keep_alive=None):
        self.rawurl=parse_url(url)
        self.url=self.rawurl.path.decode("utf-8")
        self.headers={key.decode("utf-8"):value.decode("utf-8") for key,value in  headers.items()}
        self.method=method.decode("utf-8")
        self.version=version
        self.keep_alive=keep_alive

    def setbody(self,body):
        self.body=body.decode("utf-8")