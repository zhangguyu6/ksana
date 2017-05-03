# -*- coding: utf-8 -*-
import re
from datetime import datetime

# RFC6265 http://stackoverflow.com/questions/1969232/allowed-characters-in-cookies
LegalCharsValue = r"[A-Za-z0-9!#\$%&'\*\+-\.^_`\|~]*"
LegalCharsHeader = r"[A-Za-z0-9!#$%&'\(\)\*\+-\./:<=>?@\[\]^_`\{\|\}~]*"

Translator = {n: '\\{:03o}'.format(n) for n in range(256) if not re.match(LegalCharsHeader, chr(n))}
Translator.update({
    ord('"'): '\\"',
    ord('\\'): '\\\\',
})


def _quote(header):
    # print(header)
    if not header or re.match(r"^[A-Za-z0-9]*$", header):
        return header
    else:
        return '"' + header.translate(Translator) + '"'


class Cookie(dict):
    """
    A class to hold ONE (key, value) pair.
    一个简化了的http.cookies.morsel
    """
    _reserved = {
        "expires": "expires",
        "path": "Path",
        "comment": "Comment",
        "domain": "Domain",
        "max-age": "Max-Age",
        "secure": "Secure",
        "httponly": "HttpOnly",
        "version": "Version",
    }

    _flags = {'secure',
              'httponly'
              }

    def __init__(self, key, value):
        # Set defaults
        if key in self._reserved:
            raise KeyError("Invalid Key")
        if not re.match(r"^[A-Za-z0-9]*$", key):
            raise KeyError("Illlegal key")
        # Set default attributes
        super().__init__()
        for _key in self._reserved:
            super().__setitem__(_key, "")
        for _key in self._flags:
            super().__setitem__(_key, False)
        self.key = key
        self.value = value

    def __setitem__(self, key, value):
        if key not in self._reserved:
            raise KeyError("Unknown cookie property")
        return super().__setitem__(key, value)

    def out(self):
        out = ["{}={}".format(self.key, _quote(self.value))]
        for key, value in sorted(self.items()):
            if key == "max-age" and isinstance(value, int):
                out.append("{}={}".format(self._reserved[key], value))
            elif key == "expires" and isinstance(value, datetime):
                out.append("{}={}".format(
                    self._reserved[key],
                    value.strftime("%a, %d-%b-%Y %T GMT")
                ))
            elif key in self._flags and self[key]:
                out.append(self._reserved[key])
            else:
                if value:
                    out.append("{}={}".format(self._reserved[key], value))
        return "; ".join(out)


class CookieJar(dict):
    def __init__(self):
        super(CookieJar, self).__init__()

    def __setitem__(self, key, value):
        cookie = self.get(key)
        if not cookie:
            cookie = Cookie(key, value)
        return super().__setitem__(key, cookie)


def cookiesparser(cookies):
    cookies = cookies.strip(" ")
    cookiesdict = {}
    cookielist = cookies.split(";")[:-1] if cookies[-1] == ";" else  cookies.split(";")
    for cookie in cookielist:
        pos = cookie.index("=")
        value = cookie[pos + 1:].strip(" ") if ";" not in cookie[pos + 1:] else cookie[pos + 1:cookies.index(";")]
        cookiesdict[cookie[:pos].strip(" ")] = value
    return cookiesdict

    # cookies="sdfsdfsdf=sfsdfsfsdf; _xsrf=2|972dbe8e|478161f590ba6dca7d86f24c1b6ed0d9|1492335497; "
    # print(cookiesparser(cookies))
