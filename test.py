# -*- coding: utf-8 -*-
import session
from ksana import Ksana
from response import Response

myfirstapp=Ksana()


def hello(request):
    request.usersession["mysession"] = "session"
    response = Response("<!DOCTYPE html>"
                    "<html>"
                    "<head>"
                    "<title>这是标题</title>"
                    "</head>"
                    "<body>"
                    "<p>Hello world!</p>"
                    "</body>"
                        "</html>", {}, content_type="text/html; charset=utf-8")
    response.set_cookie("sdfsdfsdf", "sfsdfsfsdf")
    response.cookies["sdfsdfsdf"]["path"] = "/helloworld"
    return response


def nothello(request):
    print("nothehello")
    print(session.SessionDict)
    print("nothehello")
    response = Response("<!DOCTYPE html>"
                        "<html>"
                        "<head>"
                        "<title>这是标题</title>"
                        "</head>"
                        "<body>"
                        "<p>not Hello world!</p>"
                        "</body>"
                        "</html>", {}, content_type="text/html; charset=utf-8")
    print(request.cookiedict)
    value = request.cookiedict.get("sdfsdfsdf")
    if value:
        response.set_cookie("sdfsdfsdf", value)
        response.delete_cookie("sdfsdfsdf")
    print("end")
    return response


myfirstapp.route.add(r"^/helloworld$", hello)
myfirstapp.route.add(r"^/nothello$", nothello)
myfirstapp.beforeresponse.append(session.SessionInterface.open)
myfirstapp.afterresponse.append(session.SessionInterface.save)
myfirstapp.run(("localhost",8888))
