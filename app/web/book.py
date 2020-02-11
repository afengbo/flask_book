#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/09 16:51'
from flask import jsonify, request

from app.forms.book import SearchForm
from . import web

from helper import is_isbn_or_key
from yushu_book import YuShuBook


@web.route('/book/search')
def search():
    """
    图书检索视图
    :param q: isbn 或者 关键字
    :param page: 页数
    :return:
    """
    search_form = SearchForm(request.args)
    if search_form.validate():
        q = search_form.q.data.strip()
        page = search_form.page.data
        isbn_or_key = is_isbn_or_key(q)
        if isbn_or_key == 'isbn':
            result = YuShuBook.search_by_isbn(q)
        else:
            result = YuShuBook.search_by_keyword(q, page)
        return jsonify(result)
    else:
        return jsonify({'msg': 'noting..'})
    # return json.dumps(result), 200, {'content-type': 'application/json'}

