from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    #path('myinfo/', views.myinfo, name = 'myinfo'),
    path('orderbook/', views.orderbook, name = 'orderbook'),
    #path('balance/', views.balance, name = 'balance')
]