#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/19 16:24'

# from collections import namedtuple

from app.view_models.books import BookViewModel

# MyGift = namedtuple('MyGift', ['id', 'book', 'wishes_count'])


class MyGifts:
    def __init__(self, my_all_gifts, book_wishes_count_list):
        self.gifts = []
        self.__my_all_gifts = my_all_gifts
        self.__book_wishes_count_list = book_wishes_count_list
        self.gifts = self.__parse()

    def __parse(self):
        temp_gifts = []
        for gift in self.__my_all_gifts:
            my_gift = self.__matching(gift)
            temp_gifts.append(my_gift)
        return temp_gifts

    def __matching(self, gift):
        count = 0
        for wish_book in self.__book_wishes_count_list:
            if gift.isbn == wish_book["isbn"]:
                count = wish_book["count"]
        my_gift = {
            "id": gift.id,
            "book": BookViewModel(gift.book),
            "wishes_count": count
        }
        # my_gift = MyGift(gift.id, BookViewModel(gift.book), count)
        return my_gift
