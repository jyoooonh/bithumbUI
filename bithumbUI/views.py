from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import API
import time
from xcoin_api_client1 import *
import requests

nonce = str(round(time.time() * 1000))
print(nonce)

apikey = ""
seckey = ""
#apikey = "9e725e6a876168c694eb5235e45b9980"
#seckey = "4e6cd21b006383c0787763405fc2a1dc"

@csrf_exempt
def index(request):
    asks_price_ratio = []
    bids_price_ratio = []

    trade_price, opening_price, min_price, max_price, trade_volume \
    = coin_info(f"https://api.bithumb.com/public/ticker/BTC_KRW")

    asks_price, asks_quantity, bids_price, bids_quantity \
        = orderbook(f"https://api.bithumb.com/public/orderbook/BTC_KRW")

    for i in range(0, 30):
        asks_price_ratio.append(((int(asks_price[i]) / int(opening_price)) - 1) * 100)
    
    for i in range(0, 30):
        bids_price_ratio.append((int(bids_price[i]) / int(opening_price) - 1) * 100)
    
    return render(request, 'bithumbUI/bithumb.html', \
    {'trade_price':trade_price, 'opening_price':opening_price, \
    'min_price':min_price, 'max_price':max_price,'trade_volume':trade_volume, \
    'asks_price': asks_price, 'asks_quantity' : asks_quantity,\
    'bids_price': bids_price, 'bids_quantity': bids_quantity,\
    'asks_price_ratio': asks_price_ratio, 'bids_price_ratio':bids_price_ratio})

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

    response = requests.get(url, headers = headers)
    response_json = response.json()

    trade_price = response_json['data']['closing_price']
    opening_price = response_json['data']['opening_price']
    min_price = response_json['data']['min_price']
    max_price = response_json['data']['max_price']
    trade_volume = response_json['data']['acc_trade_value_24H']

    return trade_price, opening_price, min_price, max_price, trade_volume