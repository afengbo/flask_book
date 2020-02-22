#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/09 10:47'
# 比较机密的配置，不要上传到git

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:111111@localhost:3306/yushu'
SECRET_KEY = 'QAZPLMXCVBN'

# Email 配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = 'xxx@qq.com'
MAIL_PASSWORD = 'xxx'
MAIL_SUBJECT_PREFIX = '[鱼书] '
# MAIL_SENDER = '鱼书 <hello@yushu.im>'
