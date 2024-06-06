from django.db import models

# Create your models here.

class CoinMarketCap(models.Model):
    acronym = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    marketCap = models.DecimalField(max_digits=20,decimal_places=2)
    volume = models.DecimalField(max_digits=20,decimal_places=2)
    circulatingSupply = models.DecimalField(max_digits=20,decimal_places=2)

    def __str__(self):
        return self.name