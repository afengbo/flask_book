#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/14 15:52'
import threading

import time
from werkzeug.local import Local, LocalStack

t = LocalStack()
t.push(1)


def func():
    print("func :", t.top)
    t.push(2)
    print("func ...", t.top)


nt = threading.Thread(target=func)
nt.start()
time.sleep(1)
print("main threading", t.top)
