from django.db import models

# Create your models here.

class CoinMarketCap(models.Model):
    acronym = models.CharField(max_length=100)
    contracts = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    price_change = models.CharField(max_length=100,default='')
    market_cap = models.CharField(max_length=100)
    market_cap_rank = models.CharField(max_length=100)
    volume = models.CharField(max_length=100)
    volume_rank = models.CharField(max_length=100)
    volume_change = models.CharField(max_length=100)
    circulating_supply = models.CharField(max_length=100)
    total_supply = models.CharField(max_length=100)
    diluted_market_cap = models.CharField(max_length=100)
    official_links = models.CharField(max_length=100,default='')
    socials = models.CharField(max_length=100,default='')
    

    def __str__(self):
        return self.name