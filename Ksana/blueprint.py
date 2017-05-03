# -*- coding: utf-8 -*-
class Blueprint:
    """
    一个简单的蓝图,只实现了延迟添加路由的功能
    """

    def __init__(self, app, prefixurl=None):
        self.app = app
        self.prefixurl = prefixurl
        self.addtasklist = []

    def add(self, urlregex, handler, handlername=None, methods=["GET"]):
        if self.prefixurl:
            if not urlregex.startswith(r"^/"):
                urlregex = r"^/" + self.prefixurl + "/" + urlregex[1:]
            else:
                urlregex = r"^" + self.prefixurl + urlregex[1:]
        args = (urlregex, handler, handlername, methods)
        self.addtasklist.append(args)

    def register(self):
        for args in self.addtasklist:
            self.app.route.add(*args)
