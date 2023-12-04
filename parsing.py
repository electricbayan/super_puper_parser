from bs4 import BeautifulSoup
import requests
from time import sleep
import sqlite3


# Функции парсинга
def parse_cian_pages(pages: int, connect, time_wait=2) -> None:
    """
    Функция для парсинга какого-то кол-ва страниц Циана
    pages - кол-во страниц для парсинга
    time_wait - время ожидания между запросами
    Возвращает словарь формата:
    {flat_id: {price: int, link: str, address: str, description: str, total_square: float, living_square: float,
    type: str}}
    """
    cursor = connect.cursor()

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
            price = int(price[:-1])

            address = []
            description = []
            for k in parser2.find_all('a', {'data-name': "AddressItem"}):
                address.append(k.text)
            for k in parser2.find_all('h1'):
                description.append(k.text)

            squares = []  # Площади квартир (жилая и общая)

            for k in parser2.find_all('div', {'data-name': 'ObjectFactoidsItem'})[:2]:
                res = ''
                for symb in k.text:
                    if symb.isdigit() or symb == ',':
                        res += symb
                squares.append(res[:-1].replace(',', '.'))

            total_square = float(squares[0])
            living_square = float(squares[1])

            flat_type = parser2.find('div', {'data-name': "OfferSummaryInfoItem"}).text[9:]

            cursor.execute(f"""INSERT INTO flats(flat_id, price, link, address, desc, total_square, living_square, type) 
                    VALUES({flat_id}, {price}, "{link}", "{address}", "{description}", 
                    "{total_square}", "{living_square}", "{flat_type}")""")

            sleep(time_wait)  # Ожидание между запросами
    connect.commit()


def parse_shops(name: str, connect) -> None:
    """
    Функция для парсинга магазинов по названию
    """
    req = requests.get(f'https://ufo.spr.ru/ekaterinburg/branches/{name}/')
    parser = BeautifulSoup(req.text, 'lxml')
    cursor = connect.cursor()

    addresses = []

    for i in parser.find_all('div', {'class': "col"}):  # Ищем все теги
        res = i.text
        if res.startswith(' Екатеринбург') and len(res) > 15:  # Если удовлетворяет условию, то заносим в бд
            res = res.replace(' г.', '').replace(' ул.', '').replace(' бульв.', '')
            res = res.replace(' пер.', '').replace(' просп.', '').strip()
            addresses.append(res)
            cursor.execute(f"""INSERT INTO shops(address, type) VALUES('{res}', '{name}')""")

    connect.commit()


if __name__ == '__main__':
    con = sqlite3.connect('db.sqlite')
    # t = time()  # Замеряем время выполнения
    # parse_cian_pages(1, con)
    # print('Time passed for shops parsing:', time() - t)

    shops = ['diksi', 'magnit', 'vernyi', 'ariant', 'pyaterochka']
    for shop_name in shops:
        parse_shops(shop_name, con)

    con.close()
