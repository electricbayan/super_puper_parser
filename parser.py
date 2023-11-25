from bs4 import BeautifulSoup as bs
import requests
import asyncio
from time import sleep, time
from pprint import pprint


def parse_names_only():
    names = []
    for j in range(1, 11):
        url = f'https://ekb.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={j}&region=4743&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1'
        req = requests.get(url)
        parser = bs(req.text, 'lxml')
        for i in parser.find_all('span', {'data-mark': "OfferTitle"}):
            names.append(i.text)
        sleep(3)
    return names


def parse_links_and_address(pages, time_wait=5):
    d = {}
    for j in range(pages):
        url = f'https://ekb.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={j}&region=4743&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1'
        req = requests.get(url)
        parser = bs(req.text, 'lxml')
        for i in parser.find_all('a', {'class': "_93444fe79c--link--eoxce"}):
            link = i['href']
            flat_id = link[link.find('flat') + 5:-1]
            req = requests.get(link)
            parser2 = bs(req.text, 'lxml')
            price = parser2.find('div', {'data-testid': "price-amount"}).text.replace('\xa0', '').replace(' ', '')
            d[flat_id] = dict()
            d[flat_id]['price'] = price[:-1]
            d[flat_id]['link'] = link

            d[flat_id]['address'] = []
            for k in parser2.find_all('a', {'data-name': "AddressItem"}):
                d[flat_id]['address'].append(k.text)

        sleep(time_wait)
    return d  # returns dict{flat_id: {price: value}}


def main():
    t = time()
    task1 = parse_links_and_address(7, time_wait=3)
    for i in task1.keys():
        print('Flat id:', i)
        print('Flat price:', task1[i]['price'])
        print('Address:', ', '.join(task1[i]['address']))
        print('Cian link:', task1[i]['link'])
        print('----------')

    print('Time:', time() - t)


if __name__ == '__main__':
    main()
