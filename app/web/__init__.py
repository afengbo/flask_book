#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/11 9:07'
from flask import Blueprint

web = Blueprint('web', __package__)

from app.web import book
