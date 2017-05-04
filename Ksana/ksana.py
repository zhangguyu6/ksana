# -*- coding: utf-8 -*-
import asyncio
import traceback
from inspect import getmodulename, currentframe, getframeinfo
from inspect import isawaitable
from signal import signal,SIGTERM, SIGINT

from Ksana.errors import ErrorHandler, KsanaError
from .baseserver import start_server
from .route import Route


class Ksana:
    def __init__(self, name=None, route=None, error_handle=None):
        self.name = name if name else getmodulename(getframeinfo(currentframe()).filename)
        self.route = route if route else Route()
        self.error_handle = error_handle if error_handle else ErrorHandler()
        #每个app维持一个队列,暂不考虑多进程的情况
        self.loop=asyncio.new_event_loop()
        self.beforeresponse = []
        self.afterresponse = []

    async def handle_request(self,request,write):
        try:
            handler, args, kwargs = self.route.get(request)
            for before in self.beforeresponse:
                before(request)
            response = handler(request, *args, **kwargs)
            for after in self.afterresponse:
                after(request, response)
            if isawaitable(response):
                print("isawaitable")
                response = await response
                print("adada")
        except KsanaError as e:
                #暂时只实现了404,405,500,没有定义异常视图的情况下,默认500
                response = self.error_handle.response(request, e)
        except Exception as e:
            print(repr(e))
            traceback.print_exc()

        write(response)

    def run(self,address,
                 request_time=10,
                 backlog=100,
                 reuse_port=False):
        signal(SIGTERM, self.loop.stop)
        signal(SIGINT, self.loop.stop)
        start_server(address=address,
                     requesthandle=self.handle_request,
                     request_time=request_time,
                     backlog=backlog,
                     reuse_port=reuse_port)
