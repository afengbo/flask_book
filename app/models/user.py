#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/18 8:51'
from math import floor

from flask import current_app
from flask_login import UserMixin
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.libs.enums import PendingStatus
from app.libs.helper import is_isbn_or_key
from app.models.base import Base, db
from app import login_manager
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook


class User(Base, UserMixin):
    __tablename__ = 'user'
    # __bind_key__ = 'fisher'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    _password = Column('password', String(128), nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    def can_save_to_db(self, isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False
        # - 不允许一个用户同时赠送多本相同的图书
        # - 不允许一个用户同时是赠送者又是索要者
        # => 这本图书既不在赠送清单中，也不在索要清单中
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False

    def generate_token(self, expiration=600):
        # 序列化器
        S = Serializer(current_app.config['SECRET_KEY'], expiration)
        return S.dumps({"id": self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        S = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = S.loads(token.encode('utf-8'))
        except Exception:
            return False
        uid = data.get("id")
        with db.auto_commit():
            user_obj = User.query.get(uid)
            user_obj.password = new_password
        return True

    def can_send_drift(self):
        if self.beans < 1:
            return False
        success_gifts_count = Gift.query.filter_by(
            uid=self.id, launched=True).count()
        success_receive_count = Drift.query.filter_by(
            requester_id=self.id, pending=PendingStatus.Success).count()
        return True if \
            floor(success_receive_count / 2) <= floor(success_gifts_count) \
            else False

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
        )


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))