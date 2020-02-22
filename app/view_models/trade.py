#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/19 10:22'
from app.view_models.books import BookViewModel


class TradeInfo:
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)

    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    def __map_to_trade(self, single):
        if single.create_time:
            time = single.create_datetime.strftime("%Y-%m-%d")
        else:
            time = "未知"
        return dict(
            user_name=single.user.nickname,
            time=time,
            id=single.id
        )


class MyTrades:
    def __init__(self, my_all_trades, book_trades_count_list):
        self.trades = []
        self.__my_all_trades = my_all_trades
        self.__book_trades_count_list = book_trades_count_list
        self.trades = self.__parse()

    def __parse(self):
        temp_trades = []
        for trade in self.__my_all_trades:
            my_trade = self.__matching(trade)
            temp_trades.append(my_trade)
        return temp_trades

    def __matching(self, trade):
        count = 0
        for trade_book in self.__book_trades_count_list:
            if trade.isbn == trade_book["isbn"]:
                count = trade_book["count"]
        my_trade = {
            "id": trade.id,
            "book": BookViewModel(trade.book),
            "trades_count": count
        }
        return my_trade
