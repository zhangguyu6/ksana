## Ksana
___
[![version](https://img.shields.io/badge/pypi-v0.0.2.2-blue.svg)](https://pypi.python.org/pypi/ksana/0.0.2.2)

Ksana是一个基于asyncio的轻量级异步web框架
### quick start
```python
 # -*- coding: utf-8 -*-
from ksana import Ksana
from response import Response

myfirstapp=Ksana()


def hello(request):
    response = Response("<!DOCTYPE html>"
                    "<html>"
                    "<head>"
                    "<title>这是标题</title>"
                    "</head>"
                    "<body>"
                    "<p>Hello world!</p>"
                    "</body>"
                        "</html>", {}, content_type="text/html; charset=utf-8")
    return response

myfirstapp.route.add(r"^/helloworld$", hello)
myfirstapp.run()
```


