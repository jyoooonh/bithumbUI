from django.db import models
import requests

class API(models.Model):
    api_key = models.CharField(max_length=50)
    secret_key = models.CharField(max_length=50)
