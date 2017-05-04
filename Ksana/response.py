# -*- coding: utf-8 -*-
import datetime
import json

from Ksana.cookies import CookieJar

STATUSDICT = {
    100: "Continue",
    200: "OK",
    302: "FOUND",
    401: "UNAUTHORIZED",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",

}


class Response:
    charset = "utf-8"
    default_status = 200
    default_mimetype = "text/plain"
    default_version = "1.1"

    def __init__(self, body=None, headers=None, version=None, status=None, content_type=None, keep_live=None,
                 encode=None):
        self.version = version if version else self.default_version
        self.status = status if status else self.default_status
        self.date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        self.content_type = content_type if content_type else self.default_mimetype
        self.keep_live = keep_live if keep_live else  ""
        self.headers = headers if headers else {}
        self.cookies = CookieJar()
        self.body = body if body else ""
        self.encode = encode

    def make_response(self):
        if self.encode:
            return self.encode_make_response()
        headerofkeeplive = "Keep-Alive: timeout={}\r\n".format(self.keep_live) if self.keep_live else ""
        baseresponse = "HTTP{version:} {status:} {statusresponse:}\r\n" \
                       "Date: {date:}\r\n" \
                       "Content-Type: {content_type:}\r\n" \
                       "Content-Length: {length:}\r\n" \
                       "Connction:{keeplive:}\r\n{keepliveset:}" \
                       "{headers:}" \
                       "{cookies:}" \
                       "\r\n{body}".format(
            version=self.version,
            status=self.status,
            statusresponse=STATUSDICT[self.status],
            date=self.date,
            content_type=self.content_type + ((" ;" + self.charset) if self.content_type == "text/plain" else ""),
            length=len(self.body),
            keeplive='keep-alive' if self.keep_live else 'close',
            keepliveset=headerofkeeplive,
            headers="\r\n".join(
                "{}: {}".format(key, value) for key, value in self.headers.items()) + "\r\n" if self.headers else "",
            cookies="\r\n".join("Set-Cookie: {}".format(self.cookies[cookie].out()) for cookie in self.cookies) + (
                " \r\n" if self.cookies else ""),
            body=self.body,
        )
        return baseresponse.encode("utf-8")

    def set_cookie(self, key, value):
        return self.cookies.__setitem__(key, value)

    def delete_cookie(self, key, request, path='/', domain=None):
        print("start delete cookies")
        if not request.cookiedict.get(key):
            return
        value = request.cookiedict[key]
        self.set_cookie(key, value)
        self.cookies[key]["path"] = path
        if domain:
            self.cookies[key][domain] = domain
        self.cookies[key]["expires"] = "0"
        self.cookies[key]["max-age"] = "0"
        print(self.cookies)
        print("end")

    def encode_make_response(self):
        headerofkeeplive = "Keep-Alive: timeout={}\r\n".format(self.keep_live) if self.keep_live else ""
        baseresponse = "HTTP{version:} {status:} {statusresponse:}\r\n" \
                       "Date: {date:}\r\n" \
                       "Content-Type: {content_type:}\r\n" \
                       "Content-Length: {length:}\r\n" \
                       "Content-Encoding: {encode}\r\n" \
                       "Connction:{keeplive:}\r\n{keepliveset:}" \
                       "{headers:}" \
                       "{cookies:}".format(
            version=self.version,
            status=self.status,
            statusresponse=STATUSDICT[self.status],
            date=self.date,
            content_type=self.content_type + ((" ;" + self.charset) if self.content_type == "text/plain" else ""),
            length=len(self.body),
            keeplive='keep-alive' if self.keep_live else 'close',
            keepliveset=headerofkeeplive,
            headers="\r\n".join(
                "{}: {}".format(key, value) for key, value in self.headers.items()) + "\r\n" if self.headers else "",
            cookies="\r\n".join("Set-Cookie: {}".format(self.cookies[cookie].out()) for cookie in self.cookies) + (
                " \r\n" if self.cookies else ""),
            encode=self.encode
        )
        baseresponse = baseresponse.encode("utf-8")
        return baseresponse + b"\r\n" + self.body


class Responsejson(Response):
    def __init__(self, body=None, headers=None, version=None, status=None, keep_live=None, encode=None):
        body = json.dumps(body)
        content_type = "application/json"
        self.encode = encode
        super().__init__(body=body, headers=headers, version=version, status=status, content_type=content_type,
                         keep_live=keep_live)


class Responsefile(Response):
    def __init__(self, filename=None, headers=None, version=None, status=None, content_type=None, keep_live=None,
                 encode=None):
        if not encode:
            with open(filename, "r") as file:
                body = file.read()
            content_type = content_type or "text/plain; charset=utf-8"
        else:
            with open(filename, "rb") as file:
                body = file.read()
            content_type = content_type

        self.encode = encode
        super().__init__(body=body, headers=headers, version=version, status=status, content_type=content_type,
                         keep_live=keep_live, encode=encode)


class Redirctresponse(Response):
    def __init__(self, to, body="", headers=None, version=None, status=302, content_type=None, keep_live=None,
                 encode=None):
        print("start redirct")
        headers = {"Location": to}
        super().__init__(body=body, headers=headers, version=version, status=status, content_type=content_type,
                         keep_live=keep_live, encode=encode)


class Responseheader(Response):
    def __init__(self, to, body="", headers=None, version=None, status=200, content_type=None, keep_live=None,
                 encode=None):
        super().__init__(body=body, headers=headers, version=version, status=status, content_type=content_type,
                         keep_live=keep_live, encode=encode)

    def make_response(self):
        headerofkeeplive = "Keep-Alive: timeout={}\r\n".format(self.keep_live) if self.keep_live else ""
        baseresponse = "HTTP{version:} {status:} {statusresponse:}\r\n" \
                       "Date: {date:}\r\n" \
                       "Content-Type: {content_type:}\r\n" \
                       "Content-Length: {length:}\r\n" \
                       "Connction:{keeplive:}\r\n{keepliveset:}" \
                       "{headers:}" \
                       "{cookies:}" \
            .format(
            version=self.version,
            status=self.status,
            statusresponse=STATUSDICT[self.status],
            date=self.date,
            content_type=self.content_type + ((" ;" + self.charset) if self.content_type == "text/plain" else ""),
            length=len(self.body),
            keeplive='keep-alive' if self.keep_live else 'close',
            keepliveset=headerofkeeplive,
            headers="\r\n".join(
                "{}: {}".format(key, value) for key, value in self.headers.items()) + "\r\n" if self.headers else "",
            cookies="\r\n".join("Set-Cookie: {}".format(self.cookies[cookie].out()) for cookie in self.cookies) + (
                " \r\n" if self.cookies else ""),
        )
        return baseresponse.encode("utf-8")
