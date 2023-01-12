import time

from django.shortcuts import render
from bs4 import BeautifulSoup
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
import time # import time module
def using_key():
    # This example uses Python 2.7 and the python-request library.



    url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/'
    parameters = {
        'start': '1',
        'limit': '5000',
        'convert': 'USD'
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

def update_data():
    coins_df = dict()
    """Name, Price, 1h%, 24h%, 7d%, Market Cap, Volume(24h), and
            Circulating Supply."""
    # data = using_key()
    while (1):
        print('updated database')
        url = requests.get('https://coinmarketcap.com')
        df = pd.read_html(url.text)[0].head(10)
        df = df[["Name", "Price", "Volume(24h)"]]
        df["Name"] = df["Name"].apply(lambda x: x.split(" ")[0])
        df["Price"] = df["Price"].apply(lambda x: float(x.replace(",", "").replace("$", "")))
        # df["Market Cap"] = df["Market Cap"].apply(lambda x: str(x).replace(",","").replace("$",""))
        # df["Market Cap"] = df["Market Cap"].apply(lambda x: str(x).replace(",","").replace("$",""))
        df["Volume(24h)"] = df["Volume(24h)"].apply(lambda x: str(x).split(" ")[0].replace(",", "").replace("$", ""))

        coin_name_list = CoinData.objects.all()

        for index, val in df.iterrows():
            print(val['Name'], val['Price'], val['Volume(24h)'])
            # coin_name_list.filter(coin_name=val['Name'])
            try:
                single_coin_data = CoinData.objects.get(coin_name=val['Name'])
                single_coin_data.coin_price = coin_price = val['Price']
                single_coin_data.coin_volume = val['Volume(24h)']
                single_coin_data.save()

            except single_coin_data.DoesNotExist:
                stock_list = CoinData(coin_name=val['Name'], coin_price=val['Price'], coin_volume=val['Volume(24h)'])
                stock_list.save()

        time.sleep(10)
    # df.to_csv("crypto-data.csv", index=True)

def stockPicker(request):

    t = threading.Thread(target=update_data, args=(), kwargs={})
    t.setDaemon(True)
    t.start()
    # t1 = threading.Thread(target=update_data())



    # content = requests.get(url).content
    # soup = BeautifulSoup(content, 'html.parser')
    # print(soup.prettify())
    # context = {'room_name': 'track','stockpicker': stock_picker, 'stock_data': all_stock_data}
    # context = {'room_name': 'track'}
    return render(request, 'stockpicker.html',context={})

class StockListView(ListAPIView):


    def get(self, request, format=None):

        print("request api done")
        coin_data = CoinData.objects.all()
        serializer_class = StockSerializer(coin_data,many=True)

        return Response(serializer_class.data,status= status.HTTP_200_OK)