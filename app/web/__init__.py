#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/11 9:07'
from flask import Blueprint, render_template

web = Blueprint('web', __package__)


@web.app_errorhandler(404)
def not_found(e):
    # AOP思想，在每个抛出404的地方执行以下代码
    return render_template("404.html"), 404


from app.web import book
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish
