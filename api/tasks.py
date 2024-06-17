from celery import shared_task
from bs4 import BeautifulSoup
import requests
from .models import CoinMarketCap
from django.http import JsonResponse

@shared_task
def scrape_crypto_data(acronyms):
    scraped_data = {}

    for acronym in acronyms:
        url = 'https://coinmarketcap.com/'

        response = requests.get(url)

        if response.status_code == 200:
            try:
                coin = CoinMarketCap.objects.get(acronym=acronym)


                output = {
                    'coin':acronym,
                    'output':{
                        'price': coin.price,
                        'price_change': coin.price_change,
                        'market_cap': coin.market_cap,
                        'market_cap_rank': coin.market_cap_rank,
                        'volume': coin.volume,
                        'volume_rank': coin.volume_rank,
                        'volume_change': coin.volume_change,
                        'circulating_supply': coin.circulating_supply,
                        'total_supply': coin.total_supply,
                        'diluted_market_cap': coin.diluted_market_cap,
                        'contracts': [],
                        'official_links': [],
                        'socials': [], 
                    }
                }
                scraped_data.append(output)
            except CoinMarketCap.DoesNotExist as e:
                return JsonResponse({'Error':str(e)})

        else:
            scraped_data[acronym] = {'Error': 'Failed to fetch data'}

    return scraped_data