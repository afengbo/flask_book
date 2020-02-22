#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/09 16:51'
import json

from flask import jsonify, request, render_template, flash, make_response
from flask_login import current_user

from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from app.view_models.books import BookViewModel, BookCollection
from app.view_models.trade import TradeInfo
from . import web


@web.route('/book/search')
def search():
    """
    图书检索视图
    :param q: isbn 或者 关键字
    :param page: 页数
    :return:
    """
    search_form = SearchForm(request.args)
    books = BookCollection()

    if search_form.validate():
        q = search_form.q.data.strip()
        page = search_form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        books.fill(yushu_book, q)
        # json模块的default实现了将方法实现交给使用者
        # return json.dumps(books, default=lambda o: o.__dict__)
    else:
        # return jsonify({'msg': 'noting..'})
        flash("搜索的关键字不符合要求，请重新输入...")
    # return json.dumps(result), 200, {'content-type': 'application/json'}
    return render_template("search_result.html", books=books, form=search_form)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_gifts = False
    has_wishes = False

    # 取书籍详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_gifts = True
        elif Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_wishes = True

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)
    return render_template('book_detail.html', book=book,
                           wishes=trade_wishes_model,
                           gifts=trade_gifts_model,
                           has_gifts=has_gifts, has_wishes=has_wishes)


@web.route('/test')
def test1():
    r = {
        "name": "Fone.",
        "age": 25
    }
    flash("hello", category='warning')
    flash("world", category='error')
    return render_template("base.html", data=r)


@web.route('/set/cookie')
def set_cookie():
    response = make_response("Hello world...")
    response.set_cookie("name", "Fone", 30)
    return response
