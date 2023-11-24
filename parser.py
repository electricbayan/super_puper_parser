from bs4 import BeautifulSoup as bs
import requests
import asyncio
from time import sleep


async def parse_names_only():
    names = []
    for j in range(1, 11):
        url = f'https://ekb.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={j}&region=4743&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1'
        req = requests.get(url)
        parser = bs(req.text, 'lxml')
        for i in parser.find_all('span', {'data-mark': "OfferTitle"}):
            names.append(i.text)
        await asyncio.sleep(3)
    return names


def parse_links_only():
    d = {}
    for j in range(1):
        url = f'https://ekb.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={j}&region=4743&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1'
        req = requests.get(url)
        parser = bs(req.text, 'lxml')
        for i in parser.find_all('a', {'class': "_93444fe79c--link--eoxce"}):
            link = i['href']
            flat_id = link[link.find('flat') + 5:-1]
            req = requests.get(link)
            parser2 = bs(req.text, 'lxml')
            price = parser2.find('div', {'data-testid': "price-amount"}).text
            price = price.replace('\\xa', '')
            d[flat_id] = dict()
            d[flat_id]['price'] = price[:-1]
        sleep(1)
    return d


def main():
    task1 = parse_links_only()
    for i in task1.keys():
        value = task1[i]['price'].replace(' ', '')
        print(f'{i} - {value}')


if __name__ == '__main__':
    main()
