#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/12 9:16'

from flask import Flask, current_app

app = Flask(__name__)

# ctx = app.app_context()
# ctx.push()
# a = current_app
# b = current_app.config['DEBUG']
# ctx.pop()

with app.app_context():
    a = current_app
    b = current_app.config['DEBUG']


class MyResource:
    def __enter__(self):
        print("Entering...")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb:
            print("process exception...")
        else:
            print("no exception...")
        print("Exiting...")
        # 出现异常时不会直接报错
        return True

    def query(self):
        print("Quering...")


with MyResource() as my_res:
    my_res.query()
