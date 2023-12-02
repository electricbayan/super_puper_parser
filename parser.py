from bs4 import BeautifulSoup
import requests
from time import sleep, time
import sqlite3


def parse_pages(pages: int, time_wait=2):
    """
    Функция для парсинга какого-то кол-ва страниц Циана
    pages - кол-во страниц для парсинга
    time_wait - время ожидания между запросами
    Возвращает словарь формата:
    {flat_id: {price: int, link: str, address: str, description: str, total_square: float, living_square: float,
    type: str}}
    """
    d = {}
    for j in range(pages):
        url = (f"https://ekb.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={j}&"
               f"region=4743&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1")
        page_req = requests.get(url)
        parser = BeautifulSoup(page_req.text, 'lxml')
        for i in parser.find_all('a', {'class': "_93444fe79c--link--eoxce"}):  # Парсинг каждого отдельного объявления
            link = i['href']
            flat_id = link[link.find('flat') + 5:-1]  # ID квартиры в Циане
            announcement_req = requests.get(link)
            parser2 = BeautifulSoup(announcement_req.text, 'lxml')
            price = parser2.find('div', {'data-testid': "price-amount"}).text.replace('\xa0', '').replace(' ', '')
            d[flat_id] = {}

            d[flat_id]['price'] = int(price[:-1])
            d[flat_id]['link'] = link

            d[flat_id]['address'] = []
            d[flat_id]['description'] = []
            for k in parser2.find_all('a', {'data-name': "AddressItem"}):
                d[flat_id]['address'].append(k.text)
            for k in parser2.find_all('h1'):
                d[flat_id]['description'].append(k.text)

            squares = []  # Площади квартир (жилая и общая)

            for k in parser2.find_all('div', {'data-name': 'ObjectFactoidsItem'})[:2]:
                res = ''
                for symb in k.text:
                    if symb.isdigit() or symb == ',':
                        res += symb
                squares.append(res[:-1].replace(',', '.'))

            d[flat_id]['total_square'] = float(squares[0])
            d[flat_id]['living_square'] = float(squares[1])

            ftype = parser2.find('div', {'data-name': "OfferSummaryInfoItem"}).text[9:]
            d[flat_id]['type'] = ftype

            sleep(time_wait)  # Ожидание между запросами
    return d


def parse_one(url):
    """
    Функция для парсинга одного объявления на Циане
    url - ссылка на объявление
    Возвращает словарь формата:
    {price: int, link: str, address: str, description: str, total_square: float, living_square: float, type: str}
    """
    d = {}
    req = requests.get(url)
    parser = BeautifulSoup(req.text, 'lxml')
    price = parser.find('div', {'data-testid': "price-amount"}).text.replace('\xa0', '').replace(' ', '')
    d['price'] = price[:-1]
    d['link'] = url

    d['address'] = []
    d['description'] = []
    for k in parser.find_all('a', {'data-name': "AddressItem"}):
        d['address'].append(k.text)
    for k in parser.find_all('h1'):
        d['description'].append(k.text)

    n = []
    for i in parser.find_all('div', {'data-name': 'ObjectFactoidsItem'})[:2]:
        res = ''
        for symb in i.text:
            if symb.isdigit() or symb == ',':
                res += symb
        n.append(res[:-1].replace(',', '.'))
    d['total_square'] = float(n[0])
    d['living_square'] = float(n[1])

    ftype = parser.find('div', {'data-name': "OfferSummaryInfoItem"}).text[9:]
    d['type'] = ftype
    return d


def write_to_db(d):
    """
    Функция для записи словаря в базу данных
    d - словарь из функции parse_pages
    """
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()

    for i in d.keys():
        price = d[i]['price']
        link = d[i]['link']
        address = ', '.join(d[i]['address'])
        desc = ', '.join(d[i]['description'])
        total = d[i]['total_square']
        living = d[i]['living_square']
        ftype = d[i]['type']
        print(price, link, address, desc, total, living)
        cur.execute(f"""INSERT INTO flats(flat_id, price, link, address, desc, total_square, living_square, type) 
        VALUES({i}, {price}, "{link}", "{address}", "{desc}", "{total}", "{living}", "{ftype}")""")
    con.commit()
    con.close()


if __name__ == '__main__':
    t = time()  # Замеряем время выполнения
    flats = parse_pages(53, time_wait=5)
    write_to_db(flats)
    print('Time passed:', time() - t)
