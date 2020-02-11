#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2020/02/09 15:16'

import requests


class HTTP:
    @staticmethod
    def get(url, return_json=True):
        res = requests.get(url)
        if res.status_code != 200:
            return {} if return_json else ''
        return res.json() if return_json else res.text
