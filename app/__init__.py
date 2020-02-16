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
    with app.app_context():
        db.create_all()
    return app


def register_blueprint(appli):
    from app.web.book import web
    appli.register_blueprint(web)