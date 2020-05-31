import requests
from bs4 import BeautifulSoup

URL = 'https://auto.ru/moskva/cars/ford/explorer/all/?sort=fresh_relevance_1-desc&geo_id=101064'
HEADERS = {'user_agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
                          Chrome/83.0.4103.61 Safari/537.36",
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,\
                      application/signed-exchange;v=b3;q=0.9'}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_ = 'ListingItem-module__main')

    cars = []
    rus = 'Ð\xa0ÐµÑ\x81Ñ\x82Ð°Ð¹Ð»Ð¸Ð½Ð³'
    eng = 'Restailing'
    for item in items:
       cars.append({
            'title': item.find('a', class_='Link ListingItemTitle-module__link').get_text(strip=True).replace(rus, eng),
            'link': item.find('a', class_='Link ListingItemTitle-module__link').get('href')

       })

    print(cars)
    print(len(cars))

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print(f'Error with status_code {html.status_code}')

parse()