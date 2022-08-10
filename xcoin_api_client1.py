import time
import math
import base64
import hmac, hashlib
import urllib.parse
import requests

class XCoinAPI:
	api_url = "https://api.bithumb.com";
	api_key = "9e725e6a876168c694eb5235e45b9980";
	api_secret = "4e6cd21b006383c0787763405fc2a1dc";

	def __init__(self, api_key, api_secret):
		self.api_key = api_key;
		self.api_secret = api_secret;

	def body_callback(self, buf):
		self.contents = buf;

	def microtime(self, get_as_float = False):
		if get_as_float:
			return time.time()
		else:
			return '%f %d' % math.modf(time.time())

	def usecTime(self) :
		mt = self.microtime(False)
		mt_array = mt.split(" ")[:2];
		return mt_array[1] + mt_array[0][2:5];

	def xcoinApiCall(self, endpoint, rgParams):
		# 1. Api-Sign and Api-Nonce information generation.
		# 2. Request related information from the Bithumb API server.
		#
		# - nonce: it is an arbitrary number that may only be used once.
		# - api_sign: API signature information created in various combinations values.

		endpoint_item_array = {
			"endpoint" : endpoint
		}

		uri_array = dict(endpoint_item_array, **rgParams) # Concatenate the two arrays.

		str_data = urllib.parse.urlencode(uri_array)

		nonce = self.usecTime()

		data = endpoint + chr(0) + str_data + chr(0) + nonce
		utf8_data = data.encode('utf-8')

		key = self.api_secret
		utf8_key = key.encode('utf-8')

		h = hmac.new(bytes(utf8_key), utf8_data, hashlib.sha512)
		hex_output = h.hexdigest()
		utf8_hex_output = hex_output.encode('utf-8')

		api_sign = base64.b64encode(utf8_hex_output)
		utf8_api_sign = api_sign.decode('utf-8')

		headers = {
			"Accept": "application/json",
			"Content-Type": "application/x-www-form-urlencoded",
			"Api-Key": self.api_key,
			"Api-Nonce": nonce,
			"Api-Sign": utf8_api_sign
		}

		url = self.api_url + endpoint

		r = requests.post(url, headers=headers, data=rgParams)
		return r.json()


