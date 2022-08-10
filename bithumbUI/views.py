from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import API
import time
from xcoin_api_client1 import *
import requests

nonce =

apikey = "9e725e6a876168c694eb5235e45b9980"
seckey = "4e6cd21b006383c0787763405fc2a1dc"

@csrf_exempt
def index(request):
    if request.method == 'POST':
        api = API()
        api.API_Key = request.POST['API_Key']
        api.Secret_Key = request.POST['Secret_Key']
        api.save()

        if apikey == api.API_Key and seckey == api.Secret_Key:
            return redirect('/orderbook')
        else:
            return redirect('/')

    return render(request, 'bithumbUI/api_key.html')

@csrf_exempt
def myinfo(request):
    if request.method == 'POST':
        api = API()
        api.API_Key = request.POST['API_Key']
        api.Secret_Key = request.POST['Secret_Key']
        api.save()
    return render(request, 'bithumbUI/api_key.html')

@csrf_exempt
def orderbook(request):
    url_orderbook = "https://api.bithumb.com/public/orderbook/BTC_KRW"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.get(url_orderbook, headers=headers)

    return HttpResponse(response.text)

@csrf_exempt
def balance(request):
    """
    api = XCoinAPI(apikey, seckey);

    rgParams = {
        'endpoint': '/info/balance',  # <-- endpoint가 가장 처음으로 와야 한다.
        "order_currency": "BTC",
    }
    result = api.xcoinApiCall(rgParams['endpoint'], rgParams)
    print(result)
    return HttpResponse(result)
    """
    url = "https://api.bithumb.com/info/balance"

    payload = "currency=BTC"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "api-client-type": "2",
        "Api-Key": "apikey",
        "Api-Nonce": "nonce",
        "Api-Sign": "상세 가이드 참고"
    }

    response = requests.post(url, data=payload, headers=headers)

    print(response.text)
    return HttpResponse(response.text)