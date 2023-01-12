from rest_framework import serializers
from .models import CoinData
class StockSerializer(serializers.ModelSerializer):
  class Meta:
    model = CoinData
    fields = ['id', 'coin_name','coin_price','coin_volume']