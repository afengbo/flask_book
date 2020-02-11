#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/08 16:36'

from flask import Flask, make_response

app = Flask(__name__)
app.config.from_object('config')
# print(app.config)


@app.route('/hello')
def hello():
    # 基于类的视图（即插视图）
    headers = {
        'content-type': 'text/plain',
        'location': 'https://bing.com'
    }
    # res = make_response("<h1>Hello, Flask!</h1>", 301)
    # res.headers = headers
    return "<h1>Hello, Flask!</h1>", 302, headers


app.add_url_rule('/hello', view_func=hello)

if __name__ == "__main__":
    # 生产环境是nginx+uwsgi模式部署flask
    # 加上ifm可以防止出现两个web服务器（uwsgi服务器和flask自带的app.run服务器）
    app.run(host='0.0.0.0', port=5001, debug=app.config['DEBUG'])
