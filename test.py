import sys
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import API
import time
import numpy as np
from xcoin_api_client1 import *
import requests

nonce = str(round(time.time() * 1000))
print(nonce)

@csrf_exempt
def index(request):
    api_key = str(request.POST.get('apikey'))
    sec_key = str(request.POST.get('seckey'))

    api_key = "9e725e6a876168c694eb5235e45b9980"
    sec_key = "4e6cd21b006383c0787763405fc2a1dc"

    asks_price_ratio = []
    bids_price_ratio = []

    trade_price, opening_price, min_price, max_price, trade_volume \
        = coin_info(f"https://api.bithumb.com/public/ticker/BTC_KRW")

    asks_price, asks_quantity, bids_price, bids_quantity \
        = orderbook(f"https://api.bithumb.com/public/orderbook/BTC_KRW")

    total_krw, available_krw, total_btc = balance(api_key, sec_key)

    for i in range(0, 30):
        asks_price_ratio.append(
            (int(asks_price[i]) / int(opening_price) - 1) * 100)

    for i in range(0, 30):
        bids_price_ratio.append(
            (int(bids_price[i]) / int(opening_price) - 1) * 100)

    asks_price_ratio = np.round(asks_price_ratio, 2)
    bids_price_ratio = np.round(bids_price_ratio, 2)
    price_ratio = round(((int(trade_price) / int(opening_price) - 1) * 100), 2)
    trade_volume = np.round((float(trade_volume) / 100000000), 1)

    return render(request, 'bithumbUI/bithumb.html',
                  {'trade_price': trade_price, 'opening_price': opening_price,
                   'min_price': min_price, 'max_price': max_price, 'trade_volume': trade_volume,
                   'asks_price': asks_price, 'asks_quantity': asks_quantity,
                   'bids_price': bids_price, 'bids_quantity': bids_quantity,
                   'asks_price_ratio': asks_price_ratio, 'bids_price_ratio': bids_price_ratio,
                   'price_ratio': price_ratio, 'total_krw':total_krw,
                    'available_krw':available_krw, 'total_btc':total_btc })

@csrf_exempt
def login(request):
    if request.method == 'GET':
        content = f'''
        <form action="/login" method="post">
            <p><input type="text" name = "apikey" placeholder="api key"></p>
            <p><input type="text" name = "seckey" placeholder="secret key"></p>
            <p><input type="submit"></p>
        </form>
        '''
        return HttpResponse(content)
    elif request.method == 'POST':
        global apikey, seckey
        apikey = request.POST.get('apikey')
        seckey = request.POST.get('seckey')

        api_key = "9e725e6a876168c694eb5235e45b9980"
        sec_key = "4e6cd21b006383c0787763405fc2a1dc"

        if api_key == apikey and sec_key == seckey:
            return redirect('/')

@csrf_exempt
def orderbook(url):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    bids_price = []
    bids_quantity = []
    asks_price = []
    asks_quantity = []
    asks_price_ratio = []
    bids_price_ratio = []

    response = requests.get(url, headers=headers)
    response_json = response.json()

    for i in range(0, 30):
        asks_price.append(response_json['data']['asks'][i]['price'])

    for i in range(0, 30):
        asks_quantity.append(response_json['data']['asks'][i]['quantity'])

    for i in range(0, 30):
        bids_price.append(response_json['data']['bids'][i]['price'])

    for i in range(0, 30):
        bids_quantity.append(response_json['data']['bids'][i]['quantity'])

    asks_quantity.reverse()
    asks_price.reverse()

    return asks_price, asks_quantity, bids_price, bids_quantity


@csrf_exempt
def coin_info(url):
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers)
    response_json = response.json()

    trade_price = response_json['data']['closing_price']
    opening_price = response_json['data']['opening_price']
    min_price = response_json['data']['min_price']
    max_price = response_json['data']['max_price']
    trade_volume = response_json['data']['acc_trade_value_24H']

    return trade_price, opening_price, min_price, max_price, trade_volume


@csrf_exempt
def balance(api_key, sec_key):
    api = XCoinAPI(api_key, sec_key)
    rgParams = {
        'endpoint': '/info/balance',  # <-- endpoint가 가장 처음으로 와야 한다.
        "order_currency": "BTC",
    }

    result = api.xcoinApiCall(rgParams['endpoint'], rgParams)
    total_krw = result['data']['total_krw']
    available_krw = result['data']['available_krw']
    total_btc = result['data']['total_btc']

    return total_krw, available_krw, total_btc
