#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/18 8:51'
from flask import current_app
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, desc, func
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from app.spider.yushu_book import YuShuBook


class Gift(Base):
    __tablename__ = 'gift'

    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)   # 礼物是否送出

    def is_yourself_gift(self, uid):
        return True if self.uid == uid else False

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_count(cls, isbn_list):
        from app.models.wish import Wish
        # 查询isbn对应的心愿数量
        # count_list: [(wishcount1, isbn1), (wishcount2, isbn2),...]
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(
            Wish.isbn).all()
        count_list = [{"count": w[0], "isbn": w[1]} for w in count_list]
        return count_list

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    # 对象代表一个具体的礼物
    # 类代表礼物这个事物，它是抽象的，不是具体的“一个”
    @classmethod
    def recent(cls):
        rencent_gifts = Gift.query.filter_by(launched=False).order_by(
            desc(Gift.create_time)).group_by(Gift.isbn).distinct().limit(
            current_app.config["RECENT_BOOK_COUNT"]).all()
        return rencent_gifts
