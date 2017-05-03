# -*- coding: utf-8 -*-
import asyncio
from pprint import pprint
from signal import SIGINT, SIGTERM

from httptools import HttpRequestParser

from Ksana.request import Request


class BaseServer(asyncio.Protocol):
    def __init__(self, loop, requesthandle, toggle, connections=set(), request_timeout=10):
        self.loop = loop
        self.requesthandle = requesthandle
        self.toggle = toggle
        self.connections = connections
        self.request_timeout = request_timeout

        self.timehandle = None
        self.requesthandletask = None
        # 默认请求参数
        self.ip = None
        self.parse = None
        self.url = None
        self.headers = {}
        self.body = None
        self.httpversion = None
        self.method = None
        self.request = None
        self.contentlength = 0
        self.keep_alive = False
        # print("enter init")

    #######################
    # 连接建立
    def connection_made(self, transport):
        # 将本连接加入全局的连接集合
        print("connect start")
        self.connections.add(self)
        self.transport = transport
        self.ip = transport.get_extra_info("peername")
        # self.timehandle = self.loop.call_later(self.request_timeout, self.teardown)

    def connection_lost(self, exc):
        print("connect end")
        self.connections.remove(self)
        # self.timehandle.cancel()
        self.clean()

    ########################
    # 解析数据
    def data_received(self, data):
        pprint(data.decode("utf-8"))
        self.contentlength += len(data)
        if not self.parse:
            # HttpRequestParser响应当前对象的以下方法
            # - on_url(url:byte)
            # - on_header(name: bytes, value: bytes)
            # - on_headers_complete()
            # - on_body(body: bytes)
            # - on_message_complete()
            # get_http_version(self) -> str
            # def should_keep_alive(self) -> bool:
            self.parse = HttpRequestParser(self)
        try:
            self.parse.feed_data(data)
        except HttpRequestParser as e:
            pass


    def on_url(self, url):
        self.url = url

    def on_header(self, name, value):
        self.headers[name] = value

    def on_headers_complete(self):
        self.method = self.parse.get_method()
        self.httpversion = self.parse.get_http_version()
        self.keep_alive = self.parse.should_keep_alive()
        self.request = Request(self.ip, self.url, self.headers, self.method, self.httpversion,
                               self.request_timeout if self.keep_alive else None)

    def on_body(self, body):
        # print(body)
        self.body = body
        self.request.setbody(body)

    def on_message_complete(self):
        print("parser complete")
        self.requesthandletask = self.loop.create_task(self.requesthandle(self.request, self.write))

    #########################
    # 返回响应
    def write(self, response):
        print("start write")
        self.transport.write(response.make_response())
        print("end write")
        keep_alive = self.keep_alive and not self.toggle[0]
        if not keep_alive:
            self.transport.close()
        else:
            self.clean()

    ########################
    # 清理或者关闭连接
    def clean(self):
        self.requsettask = None
        self.parse = None
        self.url = None
        self.headers = {}
        self.body = None
        self.httpversion = None
        self.methods = None
        self.request = None
        self.contentlength = 0
        self.keep_alive = False

    def teardown(self):
        if not self.parse:
            self.transport.close()
            return True
        return False


def start_server(address,
                 requesthandle,
                 request_time=10,
                 loop=None,
                 sock=None,
                 backlog=100,
                 reuse_port=False
                 ):
    if not loop:
        loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    toggle = [False]
    connections = set()
    server = lambda: BaseServer(loop, requesthandle, toggle, connections, request_time)
    server_future = loop.create_server(server, address[0], address[1], reuse_port=reuse_port, sock=sock,
                                       backlog=backlog)
    server_running = loop.run_until_complete(server_future)
    loop.add_signal_handler(SIGINT, loop.stop)
    loop.add_signal_handler(SIGTERM, loop.stop)
    try:
        print("server start at {}:{}".format(*address))
        loop.run_forever()
    finally:
        server_running.close()
        loop.run_until_complete(server_running.wait_closed())
        toggle[0] = True
        for connection in connections:
            connection.teardown()
        loop.close()
