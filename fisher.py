#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/08 16:36'

from app import create_app

app = create_app()


if __name__ == "__main__":
    # 生产环境是nginx+uwsgi模式部署flask
    # 加上ifm可以防止出现两个web服务器（uwsgi服务器和flask自带的app.run服务器）
    # print('333', id(app))
    app.run(host='0.0.0.0', port=5001, debug=app.config['DEBUG'])
