# -*- coding: utf-8 -*-
from inspect import getmodulename, currentframe, getframeinfo
from route import Route
from errors import ErrorHandler,KsanaError
from inspect import isawaitable
from baseserver import start_server
from signal import signal,SIGTERM, SIGINT
import asyncio

class Ksana:
    def __init__(self, name=None, route=None, error_handle=None):
        self.name = name if name else getmodulename(getframeinfo(currentframe()).filename)
        self.route = route if route else Route()
        self.error_handle = error_handle if error_handle else ErrorHandler()
        #每个app维持一个队列,暂不考虑多进程的情况
        self.loop=asyncio.new_event_loop()

    async def handle_request(self,request,write):
        try:
            handler,arg=self.route.get(request)
            print(handler,arg)
            response=handler(*arg)
            if isawaitable(response):
                response = await response
        except Exception as e:
            try:
                if issubclass(type(e),KsanaError):
                #暂时只实现了404,405,500,没有定义异常视图的情况下,默认500
                    response=self.error_handle.response(request,e)
            except Exception:
                print("aaaaaaaaaaaaa")
        write(response)

    def run(self,address,
                 request_time=10,
                 backlog=100,
                 reuse_port=False):
        signal(SIGTERM,lambda :self.loop.stop())
        signal(SIGINT,lambda :self.loop.stop())
        start_server(address=address,
                     requesthandle=self.handle_request,
                     request_time=request_time,
                     backlog=backlog,
                     reuse_port=reuse_port)
