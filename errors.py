#-*- coding: utf-8 -*-
from response import Response
class KsanaError(Exception):
    pass


class NotFound(KsanaError):
    status=b"404"

class MethodNotAllowed(KsanaError):
    status=b"405"

class ServerError(KsanaError):
    status=b"500"

class ErrorHandler:
    def __init__(self):
        self.errors=dict()

    def add(self,exception,handler):
        self.errors[exception]=handler

    def response(self,request,exception):
        errorhandeler=self.errors.get(exception,self.defaulthandler)

        response=errorhandeler(request,exception)
        return response

    def defaulthandler(self,request,exception):
        if issubclass(type(exception),KsanaError):
            return Response(body=None,headers={},status=exception.status).make_response()
e=ErrorHandler()
print(e.response("",NotFound()))