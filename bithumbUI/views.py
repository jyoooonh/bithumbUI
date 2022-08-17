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
    trade_price, opening_price, min_price, max_price, trade_volume = coin_info(f"https://api.bithumb.com/public/ticker/BTC_KRW")
    context = {'trade_price':trade_price, 'opening_price':opening_price, 'min_price':min_price, 'max_price':max_price,'trade_volume':trade_volume}
    return render(request, 'bithumbUI/bithumb.html', {'trade_price':trade_price, 'opening_price':opening_price, 'min_price':min_price, 'max_price':max_price,'trade_volume':trade_volume})

@csrf_exempt
def orderbook(url):
    response = requests.get(url)
    response_json = response.json()

    BTC_price = {}

    for i in range(0, len(response_json)):
        price = response_json[i]['price']
    return BTC_price
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