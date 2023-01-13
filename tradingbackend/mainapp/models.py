from django.db import models

# Create your models here.
class CoinData(models.Model):
    coin_name = models.CharField(max_length=255, unique=True)
    coin_price = models.FloatField(blank=True, null=True,default=0)
    coin_volume = models.CharField(max_length=255,blank=True, null=True,default='')
    coin_1h_per = models.CharField(max_length=255,blank=True, null=True,default='')
    coin_24h_per = models.CharField(max_length=255,blank=True, null=True,default='')
    coin_7d_per = models.CharField(max_length=255,blank=True, null=True,default='')
    coin_mkt_cap = models.CharField(max_length=255,blank=True, null=True,default='')
    coin_circulating_supply = models.CharField(max_length=255,blank=True, null=True,default='')
    # coin_volume = models.PositiveIntegerField(blank=True, null=True,default=0)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)


