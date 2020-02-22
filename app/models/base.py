#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/18 8:50'
from contextlib import contextmanager
from datetime import datetime

from flask import flash
from sqlalchemy import Column, Integer, SmallInteger
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            db.session.commit()
            flash("数据保存成功。")
        except Exception as e:
            db.session.rollback()
            return e


class Query(BaseQuery):
    # 继承基类，重写filter_by方法
    # 在查询的时候只查有效数据
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True   # 不在数据库创建真实的数据表
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def delete(self):
        self.status = 0
