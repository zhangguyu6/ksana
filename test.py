# -*- coding: utf-8 -*-
from Ksana import session, Ksana, Response

from Ksana.blueprint import Blueprint

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
    response.set_cookie("simplecookie", "123456789")
    response.cookies["simplecookie"]["path"] = "/helloworld"
    return response


def nothello(request):
    print("nothehello")
    print(session.SessionDict)
    response = Response("<!DOCTYPE html>"
                        "<html>"
                        "<head>"
                        "<title>这是标题</title>"
                        "</head>"
                        "<body>"
                        "<p>not Hello world!</p>"
                        "</body>"
                        "</html>", {}, content_type="text/html; charset=utf-8")
    value = request.cookiedict.get("simplecookie")
    if value:
        response.delete_cookie("simplecookie")
    print("end")
    return response


myblueprint = Blueprint(myfirstapp)
myblueprint.add(r"^/nothello$", nothello)

myblueprint.register()
myfirstapp.route.add(r"^/helloworld$", hello)
# myfirstapp.route.add(r"^/nothello$", nothello)
myfirstapp.beforeresponse.append(session.SessionInterface.open)
myfirstapp.afterresponse.append(session.SessionInterface.save)

myfirstapp.run(("localhost", 8889))
