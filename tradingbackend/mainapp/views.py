

from django.shortcuts import render

import requests
import pandas as pd
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from .models import CoinData
from .serializers import StockSerializer
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response
import threading
import time

def using_key():

    # url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/'
    url='https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
    parameters = {
        'start': '1',
        'limit': '10',

    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'ea2c429b-c3b6-4d96-bbf6-200a3fbdac40',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        # print(data)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def home(request):

    return render(request, 'stockpicker.html',context={})

class StockListView(ListAPIView):


    def get(self, request, format=None):

        print("request api done")
        coin_data = CoinData.objects.all()
        serializer_class = StockSerializer(coin_data,many=True)

        return Response(serializer_class.data,status= status.HTTP_200_OK)