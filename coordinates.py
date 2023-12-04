import requests
import sqlite3
from database_functions import get_flats_data_from_db, get_shops_data_from_db
from geopy.distance import geodesic


def fetch_coordinates(api_key, address):
    """
    Возвращает координаты места
    """
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": api_key,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lat, lon


if __name__ == '__main__':
    apikey = 'e9d96ce6-6d3b-4d62-9114-2185b11c9b8a'

    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()

    flats = get_flats_data_from_db(con)
    shops = get_shops_data_from_db(con)

    for shop_address in shops.keys():  # Устанавливаем координаты для магазинов
        coords = ', '.join(fetch_coordinates(apikey, shop_address))
        cur.execute(f"""UPDATE shops SET coords='{coords}' WHERE address={shop_address}""")

    for flat_id in flats.keys():  # Устанавливаем координаты для квартир
        coords = ', '.join(fetch_coordinates(apikey, flats[flat_id]['address']))
        cur.execute(f"""UPDATE flats SET coords='{coords}' WHERE flat_id={flat_id}""")

    for i in flats.keys():  # Находим ближайшие магазины у каждой квартиры
        s_count = int(cur.execute(f"""SELECT shops_nearby FROM flats WHERE flat_id={i}""").fetchone()[0])
        for j in shops.keys():
            distantion = geodesic(flats[i]['coords'], shops[j]['coords']).kilometers
            if distantion < 1:
                s_count += 1
        cur.execute(f"""UPDATE flats SET shops_nearby={s_count} WHERE flat_id={i}""")

    con.commit()
    con.close()
