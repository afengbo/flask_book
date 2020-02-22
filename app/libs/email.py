#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/20 8:50'
from threading import Thread

from flask import current_app, render_template

from app import mail
from flask_mail import Message


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass


def send_email(to, subject, template, **kwargs):
    msg = Message(current_app.config["MAIL_SUBJECT_PREFIX"] + subject,
                  sender=current_app.config["MAIL_USERNAME"],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    # current_app：LocalProxy代理对象，受线程隔离的影响。
    # 这里应该传入真实对象app
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
