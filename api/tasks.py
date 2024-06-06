from celery import shared_task
from bs4 import BeautifulSoup
import requests
from .models import CoinMarketCap

@shared_task
def scrape_crypto_data(acronyms):
    scraped_data = {}

    for acronym in acronyms:
        url = 'https://coinmarketcap.com/'

        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content,'html.parser')
            price = soup.find('span', class_='price').text.strip()
            marketCap = soup.find('span', class_='market_cap').text.strip()
            volume = soup.find('span', class_='volume-24h').text.strip()
            circulatingSupply = soup.find('span', class_='circulating-supply').text.strip()

            coin, created = CoinMarketCap.objects.get_or_create(acronym=acronym)
            coin.price = price
            coin.marketCap = marketCap
            coin.volume = volume
            coin.circulatingSupply = circulatingSupply
            coin.save()

            scraped_data[acronym] = {
                'Price': price,
                'marketCap': marketCap,
                'volume': volume,
                'circulatingSupply': circulatingSupply
            }
        else:
            scraped_data[acronym] = {'Error': 'Failed to fetch data'}

    return scraped_data