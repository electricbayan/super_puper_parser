from geopy.geocoders import Nominatim
import requests
from bs4 import BeautifulSoup
import sqlite3


def add_to_db_shops(name):
    """
    Функция для парсинга магазинов по названию
    """
    req = requests.get(f'https://ufo.spr.ru/ekaterinburg/branches/{name}/')
    parser = BeautifulSoup(req.text, 'lxml')

    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()

    addresses = []

    for i in parser.find_all('div', {'class': "col"}):  # Ищем все теги
        res = i.text
        if res.startswith(' Екатеринбург') and len(res) > 15:  # Если удовлетворяет условию. то заносим в бд
            res = res.strip().replace(' г.', '').replace(' ул.', '').replace(' бульв.', '')
            res = res.replace(' пер.', '').replace(' просп.', '')
            addresses.append(res)
            cur.execute(f"""INSERT INTO shops(address, type) VALUES('{res}', '{name}')""")

    addresses = [i[0] for i in cur.execute("""SELECT address FROM shops""").fetchall()]

    geolocator = Nominatim(user_agent="Tester")
    for address in addresses:
        old_address = address
        if address[-2] == '-':
            address = address[:-2]
        if address[-4:-2] == 'к.':
            address = address[:-6]
        location = geolocator.geocode(address)
        if location:
            cur.execute(f"""UPDATE shops SET coords='{location.latitude}; {location.longitude}' 
            WHERE address='{old_address}'""")

    con.commit()
    con.close()


if __name__ == '__main__':
    shops = ['diksi', 'magnit', 'pyaterochka', 'ariant', 'vernyi']
    for shop_name in shops:
        add_to_db_shops(shop_name)
