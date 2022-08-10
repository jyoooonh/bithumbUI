# orderbook
import requests

url_orderbook = "https://api.bithumb.com/public/orderbook/BTC_KRW"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

response = requests.get(url_orderbook, headers=headers)

print(response.text)

# API
# balance (xcoin_api_client1, api_test)
import requests

url = "https://api.bithumb.com/info/balance"

payload = "currency=BTC"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
    "Api-Key": "사용자 Access Key",
    "Api-Nonce": "현재시각(ms)",
    "Api-Sign": "상세 가이드 참고"
}

response = requests.post(url, data=payload, headers=headers)

print(response.text)

# trade place
import requests

url = "https://api.bithumb.com/trade/place"

payload = "order_currency=1&payment_currency=1&units=1&price=1&type=bid/or/ask"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
    "api-client-type": "2",
    "Api-Key": "사용자 Access Key",
    "Api-Nonce": "현재시각(ms)",
    "Api-Sign": "상세 가이드 참고"
}

response = requests.post(url, data=payload, headers=headers)

print(response.text)

# trade market buy
import requests

url = "https://api.bithumb.com/trade/market_buy"

payload = "units=1&order_currency=BTC&payment_currency=KRW"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
    "api-client-type": "2",
    "Api-Key": "사용자 Access Key",
    "Api-Nonce": "현재시각(ms)",
    "Api-Sign": "상세 가이드 참고"
}

response = requests.post(url, data=payload, headers=headers)

print(response.text)

# trade market sell
import requests

url = "https://api.bithumb.com/trade/market_sell"

payload = "units=1&order_currency=BTC&payment_currency=KRW"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
    "api-client-type": "2",
    "Api-Key": "사용자 Access Key",
    "Api-Nonce": "현재시각(ms)",
    "Api-Sign": "상세 가이드 참고"
}

response = requests.post(url, data=payload, headers=headers)

print(response.text)