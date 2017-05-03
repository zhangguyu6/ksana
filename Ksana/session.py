# -*- coding: utf-8 -*-
import uuid

global SessionDict
SessionDict = {"1": "2"}


class Usersession(dict):
    def __init__(self, uid):
        super(Usersession, self).__init__()
        self.modified = False
        self.uid = uid


class SessionInterface:
    @classmethod
    def open(self, request):
        print("open start")
        cookiesdict = request.cookiedict
        if cookiesdict:
            uid = cookiesdict.get("uid")
        print("open", SessionDict)
        if not cookiesdict or not uid or not SessionDict.get(uid):
            uid = uuid.uuid4().hex
            usersession = SessionDict[uid] = Usersession(uid)
            usersession.modified = True
        else:
            usersession = SessionDict[uid]
        request.usersession = usersession
        print(SessionDict)
        print("end start")

    @classmethod
    def save(self, request, response):
        if not request.usersession.modified:
            return
        uid = request.usersession.uid
        response.set_cookie("uid", uid)
        print("save", SessionDict)
