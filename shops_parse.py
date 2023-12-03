import time

from geopy.distance import geodesic
import sqlite3
from main import get_flats_data_from_db, get_shops_data_from_db


def distance(home_coords, shop_coords):
    distance = geodesic(home_coords, shop_coords).kilometers
    return distance


# Пример использования:
home_coords = (55.7558, 37.6176)  # координаты квартиры
shop_coordinates = [(55.7563, 37.6157), (55.7545, 37.6202), (55.7572, 37.6190)]  # координаты магазинов
radius_km = 1.0  # радиус в километрах


con = sqlite3.connect('db.sqlite')
cur = con.cursor()
flats = get_flats_data_from_db(cur)
shops = get_shops_data_from_db(cur)


for i in flats.keys():
    s_count = int(cur.execute(f"""SELECT shops_nearby FROM flats WHERE flat_id={i}""").fetchone()[0])
    for j in shops.keys():
        distantion = distance(flats[i]['coords'], shops[j]['coords'])
        if distantion < 1:
            s_count += 1
    cur.execute(f"""UPDATE flats SET shops_nearby={s_count} WHERE flat_id={i}""")
con.commit()
con.close()
