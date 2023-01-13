from rest_framework import serializers
from .models import CoinData
class StockSerializer(serializers.ModelSerializer):
  class Meta:
    model = CoinData
    fields = ['id', 'coin_name', 'coin_price', 'coin_volume', 'coin_1h_per',
              'coin_24h_per', 'coin_7d_per', 'coin_mkt_cap', 'coin_circulating_supply']