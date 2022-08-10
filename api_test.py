#! /usr/bin/env python
# XCoin API-call sample script (for Python 3.X)
#
# @author	btckorea
# @date	2017-04-11
#
#
# First, Build and install pycurl with the following commands::
# (if necessary, become root)
#
# https://pypi.python.org/pypi/pycurl/7.43.0#downloads
#
# tar xvfz pycurl-7.43.0.tar.gz
# cd pycurl-7.43.0
# python setup.py --libcurl-dll=libcurl.so install
# python setup.py --with-openssl install
# python setup.py install

import sys
from xcoin_api_client1 import *

api_key = "9e725e6a876168c694eb5235e45b9980";
api_secret = "4e6cd21b006383c0787763405fc2a1dc";

api = XCoinAPI(api_key, api_secret);

rgParams = {
    'endpoint': '/info/ticker',  #<-- endpoint가 가장 처음으로 와야 한다.
    "order_currency": "BTC",
}

result = api.xcoinApiCall(rgParams['endpoint'], rgParams)
print(result)


#잔고조회

def bithumbBalance(currency):
    rgParams = {
        "currency": currency,
    }
    result = api.xcoinApiCall("/info/balance/"+currency, rgParams)
    return result

result = bithumbBalance("ALL")
result = bithumbBalance("BTC")
print(result)
"""
# 매수
def bithumbBuy(price, qty, currency):
    rgParams = {
        "order_currency": currency,
        "units": qty,
        "price": price,
        "type": "bid"
    }
    result = api.xcoinApiCall("/trade/place", rgParams)
    print("status: " + result["status"])
    return result["status"]

result = bithumbBuy(100000,1,"BTC")
print(result)

# 매도
def bithumbSell(price, qty, currency):
    rgParams = {
        "order_currency": currency,
        "units": qty,
        "price": price,
        "type": "ask" # 매도
    }
    result = api.xcoinApiCall("/trade/place", rgParams)
    print("status: " + result["status"]) # 중요 로그
    return result["status"]

"""