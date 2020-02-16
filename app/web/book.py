#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/09 16:51'
import json

from flask import jsonify, request, render_template, flash

from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from app.view_models.books import BookViewModel, BookCollection
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
    pass


@web.route('/test')
def test1():
    r = {
        "name": "Fone.",
        "age": 25
    }
    flash("hello", category='warning')
    flash("world", category='error')
    return render_template("base.html", data=r)