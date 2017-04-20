## Ksana
___
Ksana是一个基于asyncio的轻量级异步web框架
### quick start
```
from ksana import Ksana
from response import Response

myfirstapp=Ksana()

def hello():
    return Response("<!DOCTYPE html>"
                    "<html>"
                    "<head>"
                    "<title>这是标题</title>"
                    "</head>"
                    "<body>"
                    "<p>Hello world!</p>"
                    "</body>"
                    "</html>",{},content_type="text/html; charset=utf-8").make_response()
myfirstapp.route.add("/helloworld",hello)
myfirstapp.run(("localhost",8888))
```


