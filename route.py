# -*- coding: utf-8 -*-
from collections import namedtuple
from errors import MethodNotAllowed, NotFound
import re


class route:
    def __init__(self, handler, methods, parameters):
        self.handler = handler
        self.methods = methods
        self.parameters = parameters


parameter = namedtuple("Parameter", ["name", "ty"])


class Route:
    def __init__(self):

        self.routes = {}
        self.hosts = []

    def add(self, url, handler, methods=["GET"], host=None):
        '''
        :param url: 匹配路径
        :param handler: 拦截函数
        :param methods: 方法列表
        :param host: 主机
        '''
        if host:
            self.hosts.append(host)
            absurl = host + url
        else:
            absurl = url
        if not absurl.startswith("/"):
            absurl += "/"
        if absurl in self.routes:
            pass
        parapattern = re.compile(r"(.*?)<(.*)>")
        r = re.match(parapattern, absurl)
        if r:
            parameterstr = r.group(2)
            if ":" in parameterstr:
                # 有类型下为("name","str")
                _name, _type = parameterstr.split(":")
            else:
                # 无类型下为("name","")
                _name, _type = parameterstr, ""
            absurl = r.group(1) + "<{}>".format(_type)
        else:
            parameterstr = ""
            # 无参数下为("","")
            _name, _type = parameterstr, ""
        _parameter = parameter(_name, _type)
        _route = route(handler, methods, _parameter)
        self.routes[absurl] = _route

    def _get(self, url, method, host):
        absurl = url + host
        if not absurl.startswith("/"):
            absurl += "/"
        pattern = re.compile(r"(.*/)(.+?)$")
        match = re.match(pattern, absurl)
        if match:
            firstpart = match.group(1)
            # 最后一个"/"后的字符串
            lastpart = match.group(2)
        arg = []
        # 优先匹配静态
        currentroute = self.routes.get(absurl, None)
        if currentroute:
            return currentroute.handler, arg
        # 对所有动态url以类型代替关键字
        if match:
            if re.match(r"[A-Za-z]+", lastpart):
                parapart = "<string>"
                # print(parapart)
                arg = lastpart
            elif re.match(r"\d+", lastpart):
                parapart = "<int>"
                arg = int(lastpart)
            elif re.match(r"[0-9\\.]+", lastpart):
                parapart = "<float>"
                arg = float(lastpart)
            else:
                parapart = None
            if not currentroute and parapart:
                currentroute = self.routes.get(firstpart + parapart, None)
        if not currentroute:
            raise NotFound
        if method not in currentroute.methods:
            raise MethodNotAllowed
        return currentroute.handler, arg

    def get(self, request):
        if not self.hosts:
            return self._get(request.url, request.method, '')
        else:
            return self._get(request.url, request.method,
                             request.headers.get("Host", ''))

# def printadb():
#     print("abc")
#
# myroute=Route()
# myroute.add("/hello",printadb)
# myroute.get("/hello","GET","")()
# myroute.add("/helloworld/<name:string>",printadb)
# myroute.get("/helloworld/zgy","GET","")()
