#-*- coding: utf-8 -*-
class Response:
    def __init__(self,body,headers,status=b"200",content_type="text/plain",keep_live=None):
        print("start response init")
        self.status=status
        #format不支持byte,%支持
        self.headers=b"".join(b"%b: %b"%(key.encode("utf-8"),value.encode("utf-8")) for key,value in headers.items())
        self.content_type=content_type.encode("utf-8")
        self.body=body.encode("utf-8") if body else b""
        self.keep_live=keep_live

    def make_response(self,version=b"1.1"):
        headerofkeeplive=b"Keep-Alive: timeout=%d\r\n" % self.keep_live if self.keep_live else b""
        baseresponse=b"HTTP%b %b %b\r\n" \
             b"Content-Type: %b\r\n" \
             b"Content-Length: %d\r\n" \
             b"Connction:%b\r\n%b" \
             b"%b\r\n" \
             b"\r\n%b"%(
            version,
            self.status,
            b"ok",
            self.content_type,
            len(self.body),
            b'keep-alive' if self.keep_live else b'close',
            headerofkeeplive,
            self.headers,
            self.body
        )
        return baseresponse
