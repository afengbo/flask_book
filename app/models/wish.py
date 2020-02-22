#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/18 15:11'

from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, func, desc
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from app.spider.yushu_book import YuShuBook


class Wish(Base):
    __tablename__ = 'wish'

    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)   # 礼物是否送出

    @classmethod
    def get_user_wishes(cls, uid):
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(
            desc(Wish.create_time)).all()
        return wishes

    @classmethod
    def get_gift_count(cls, isbn_list):
        from app.models.gift import Gift
        # 查询isbn对应的赠送数量
        # count_list: [(giftcount1, isbn1), (giftcount2, isbn2),...]
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False,
            Gift.isbn.in_(isbn_list),
            Gift.status == 1).group_by(
            Gift.isbn).all()
        count_list = [{"count": w[0], "isbn": w[1]} for w in count_list]
        return count_list

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first
