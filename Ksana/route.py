# -*- coding: utf-8 -*-
import re
from collections import namedtuple

from Ksana.errors import MethodNotAllowed, NotFound

route = namedtuple("route", ["endpoint", "methods"])




class Route:
    """
    采用类似djngo的正则路由匹配
    """
    def __init__(self):
        self.routes = {}
        self.endtoview = {}

    def add(self, urlregex, handler, handlername=None, methods=["GET"]):
        '''
        :param urlregex: 匹配路径
        :param handler: 拦截函数
        :param handlername: 拦截函数名
        :param methods: 支持的方法
        '''
        if not urlregex.startswith(r"^/"):
            urlregex = r"^/" + urlregex[1:]
        if not handlername:
            handlername = handler.__name__
        self.routes[urlregex] = route(handlername, methods)
        self.endtoview[handlername] = handler

    def get(self, request):
        return self._get(request.url, request.method)

    def _get(self, url, method):
        if not url.startswith("/"):
            url += "/"
        for regex in self.routes:
            matchgroup = re.match(regex, url)
            if matchgroup:
                route = self.routes[regex]
                handlername = route.endpoint
                methods = route.methods
                if method in methods:
                    kwargs = matchgroup.groupdict()
                    # urlregex中匿名捕获和非匿名捕获的顺序,必须按照先位置参数,后关键词参数的顺序排列
                    args = matchgroup.groups()[:-len(kwargs)] if kwargs else matchgroup.groups()
                    handler = self.endtoview[handlername]
                    return handler, args, kwargs
                raise MethodNotAllowed
        raise NotFound

# def printadc():
#     print("abc")
# def printanything(thing):
#     print(thing)
# def printspecialthing(thing):
#     print(thing)
# myroute=Route()
# myroute.add(r"^/hello$",printadc)
# handler,args,kwargs=myroute.get("/hello","GET")
# handler(*args,*kwargs)
# myroute.add(r"^/hello/(.+?)$",printanything)
# handler,args,kwargs=myroute.get("/hello/adad","GET")
# handler(*args,*kwargs)
# myroute.add(r"^/helloworld/(?P<thing>.+?)$",printspecialthing)
# handler,args,kwargs=myroute.get("/helloworld/somethingspecial","GET")
# handler(*args,*kwargs)
