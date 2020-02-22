#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/18 17:02'
# 在执行核心代码前后执行其他代码
from contextlib import contextmanager


@contextmanager
def ctx():
    print("《", end="")
    yield
    print("》", end="")


with ctx():
    print("情书", end="")
