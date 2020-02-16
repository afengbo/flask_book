#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/16 9:26'

class BookViewModel:
    def __init__(self, data):
        self.title = data['title']
        self.publisher = data['publisher']
        self.pages = data['pages']
        self.authors = "、".join(data['author'])
        self.price = data['price']
        self.summary = data['summary']
        self.image = data['image']


class BookCollection:
    def __init__(self):
        self.total = 0
        self.keyword = ''
        self.books = []

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]


# class _BookViewModel:
#     @classmethod
#     def package_single(cls, data, keyword):
#         ret = {
#             "books": [],
#             "total": 0,
#             "keyword": keyword
#         }
#         if data:
#             ret["total"] = 1
#             ret["books"] = [cls.__cut_book_data(data)]
#         return ret
#
#     @classmethod
#     def package_collection(cls, data, keyword):
#         ret = {
#             "books": [],
#             "total": 0,
#             "keyword": keyword
#         }
#         if data:
#             ret["total"] = data["total"]
#             ret["books"] = [cls.__cut_book_data(book) for book in data['books']]
#         return ret
#
#     @classmethod
#     def __cut_book_data(cls, data):
#         book = {
#             "title": data['title'],
#             "publisher": data['publisher'],
#             "pages": data['pages'] or "",
#             "authors": "、".join(data['authors']),
#             "price": data['price'],
#             "summary": data['summary'] or "",
#             "image": data['image'],
#         }
#         return book
