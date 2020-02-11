#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/11 9:08'
from flask import Flask
from app.models.book import db


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)
    db.init_app(app)
    db.create_all(app=app)
    return app


def register_blueprint(app):
    from .web.book import web
    app.register_blueprint(web)