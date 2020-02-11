#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/09 15:02'

def is_isbn_or_key(word):
    """
    判断isbn还是关键字搜索
    :param word:
    :return: isbn_or_key
    """
    # isbn13： 由13个0-9的数字组成
    # isbn10：由10个0-9的数字组成，含有"-"
    isbn_or_key = 'key'
    if len(word) == 13 and word.isdigit():
        isbn_or_key = 'isbn'
    short_word = word.replace('-', '')
    if '-' in word and len(short_word) == 10 and short_word.isdigit():
        isbn_or_key = 'isbn'
    return isbn_or_key
