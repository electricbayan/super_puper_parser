import sqlite3
import requests


def get_flats_data_from_db(cursor):
    """
    Функция для получения словаря из базы данных
    Возвращает словарь формата:
    {flat_id: {price: int, address: str, total_square: float, living_square: float, type: str, district: str}}
    """
    d = {}
    for string in cursor.execute("""SELECT * FROM flats"""):
        d[string[0]] = {}
        d[string[0]]['price'] = int(string[1])
        d[string[0]]['address'] = string[3]
        d[string[0]]['total_square'] = string[5]
        d[string[0]]['living_square'] = string[6]
        d[string[0]]['type'] = string[7]
        d[string[0]]['district'] = string[3].split(', ')[2]
    return d


def fetch_coordinates(api_key, address):
    """
    Возвращает координаты дома
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

    flats = get_flats_data_from_db(cur)
    coords_dict = {}
    keys = list(flats.keys())

    for i in keys[:800]:
        coords = fetch_coordinates(apikey, flats[i]['address'])
        coords_dict[i] = '; '.join(coords)
    for i in coords_dict.keys():
        cur.execute(f"""UPDATE flats SET coords='{coords_dict[i]}' WHERE flat_id={i}""")
    con.commit()
    con.close()
