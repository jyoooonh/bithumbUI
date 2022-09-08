import sys
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import API
import time
import numpy as np
from xcoin_api_client1 import *
import requests
from django.contrib import messages

nonce = str(round(time.time() * 1000))
print(nonce)

apikey = "9e725e6a876168c694eb5235e45b9980"
seckey = "4e6cd21b006383c0787763405fc2a1dc"

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
def index(request):
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

    if request.method == 'GET':
        return render(request, 'bithumbUI/bithumb.html',
                  {'trade_price': trade_price, 'opening_price': opening_price,
                   'min_price': min_price, 'max_price': max_price, 'trade_volume': trade_volume,
                   'asks_price': asks_price, 'asks_quantity': asks_quantity,
                   'bids_price': bids_price, 'bids_quantity': bids_quantity,
                   'asks_price_ratio': asks_price_ratio, 'bids_price_ratio': bids_price_ratio,
                   'price_ratio': price_ratio, 'total_krw':total_krw,
                    'available_krw':available_krw, 'total_btc':total_btc })
    elif request.method == 'POST':
        ordertype = request.POST.getlist('ordertype')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        bs = request.POST.getlist('bs')
        print(ordertype,price,quantity,bs)
        if ordertype[0]=='limit':
            if bs[0]=='buy':
                if float(total_krw) < float(price)*float(quantity):
                    #매수 불가
                    messages.error(request,'원화가 부족하여 매수할 수 없습니다')
                    print('원화가 부족하여 매수할 수 없습니다')
                else:
                    #매수 실행
                    limitbuynsell(api_key,sec_key,float(quantity),int(price),'bid')
                    messages.success(request,'매수 주문이 완료되었습니다')
                    print('매수 주문이 완료되었습니다')
            elif bs[0]=='sell':
                if float(total_btc) < float(quantity):
                    #매도 불가
                    messages.error(request,'보유 자산 수량이 목표 매도 금액보다 적습니다')
                    print('보유 자산 수량이 목표 매도 금액보다 적습니다')
                else:
                    #매도 실행
                    limitbuynsell(api_key,sec_key,float(quantity),int(price),'ask')
                    messages.success(request,'매도 주문이 완료되었습니다')
                    print('매도 주문이 완료되었습니다')
            else:
                #에러
                messages.error(request,'알 수 없는 이유로 에러가 발생했습니다')
                print('알 수 없는 이유로 에러가 발생했습니다')
        elif ordertype[0]=='market':
            if bs[0]=='buy':
                if float(total_krw) < '''현재가'''*float(quantity):
                    #매수 불가
                    messages.error(request,'원화가 부족하여 매수할 수 없습니다')
                    print('원화가 부족하여 매수할 수 없습니다')

                else:
                    #매수 실행
                    marketbuynsell(api_key,sec_key,float(quantity),'bid')
                    messages.success(request,'매수 주문이 완료되었습니다')
                    print('매수 주문이 완료되었습니다')
            elif bs[0]=='sell':
                if float(total_btc) < float(quantity):
                    #매도 불가
                    messages.error(request,'보유 자산 수량이 목표 매도 금액보다 적습니다')
                    print('보유 자산 수량이 목표 매도 금액보다 적습니다')
                else:
                    #매도 실행
                    marketbuynsell(api_key,sec_key,float(quantity),'ask')
                    messages.success(request,'매도 주문이 완료되었습니다')
                    print('매도 주문이 완료되었습니다')
            else:
                #에러
                messages.error(request,'알 수 없는 이유로 에러가 발생했습니다')
                print('알 수 없는 이유로 에러가 발생했습니다')
        else:
            #매수/매도가 아닌경우 에러
            messages.error(request,'매수/매도 주문이 아닙니다')
        return redirect('/bithumbUI')


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

@csrf_exempt
def limitbuynsell(api_key,sec_key,units,price,type):
    api = XCoinAPI(api_key, sec_key)
    rgParams = {
        'endpoint': '/trade/place',  # <-- endpoint가 가장 처음으로 와야 한다.
        "order_currency" : "BTC",
        "payment_currency" : "KRW",
        "units" : units,
        "price" : price,
        "type" : type
    }
    result = api.xcoinApiCall(rgParams['endpoint'], rgParams)
    print(result)

def marketbuynsell(api_key,sec_key,units,type):
    api = XCoinAPI(api_key, sec_key)
    bsurl=""
    if type=="bid":
        bsurl = "/trade/market_buy"
    elif type=="ask":
        bsurl="/trade/market_sell"
    rgParams = {
        'endpoint': bsurl,  # <-- endpoint가 가장 처음으로 와야 한다.
        "units" : units,
        "order_currency" : "BTC",
        "payment_currency" : "KRW"
    }
    result = api.xcoinApiCall(rgParams['endpoint'], rgParams)
    print(result)