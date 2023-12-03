import sqlite3
import matplotlib.pyplot as plt

def get_flats_data_from_db(cursor):
    """
    Функция для получения словаря из базы данных flats
    Возвращает словарь формата:
    {flat_id: {price: int, address: str, total_square: float, living_square: float, type: str, district: str, coords: str, shops_nearby: int}}
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
        d[string[0]]['coords'] = string[8].replace(';', ',')
        d[string[0]]['shops_nearby'] = int(string[9])

    return d

def plot_shops_nearby_by_district(flats_data):
    districts = set(flat['district'] for flat in flats_data.values())
    district_counts = {district: sum(flat['shops_nearby'] for flat in flats_data.values() if flat['district'] == district) for district in districts}

    # Сортируем районы по количеству магазинов
    sorted_districts = sorted(district_counts.keys(), key=lambda x: district_counts[x], reverse=True)

    # Устанавливаем размер фигуры
    plt.figure(figsize=(10, 10))

    # Построение столбчатой диаграммы с установкой нижней границы
    plt.bar(sorted_districts, [district_counts[district] for district in sorted_districts], bottom=0.3)
    plt.title('Зависимость количества магазинов от района')
    plt.xlabel('Район')
    plt.ylabel('Количество магазинов')
    plt.xticks(rotation=45, ha="right")  # Поворот меток по оси X для лучшей читаемости

    plt.show()

# Подключение к базе данных SQLite
con = sqlite3.connect('db.sqlite')
cur = con.cursor()

# Извлечение данных о квартирах из базы данных
flats_data = get_flats_data_from_db(cur)

# Построение столбчатой диаграммы зависимости количества магазинов от района
plot_shops_nearby_by_district(flats_data)



# def fetch_coordinates(api_key, address):
#     """
#     Возвращает координаты дома
#     """
#     base_url = "https://geocode-maps.yandex.ru/1.x"
#     response = requests.get(base_url, params={
#         "geocode": address,
#         "apikey": api_key,
#         "format": "json",
#     })
#     response.raise_for_status()
#     found_places = response.json()['response']['GeoObjectCollection']['featureMember']
#
#     if not found_places:
#         return None
#
#     most_relevant = found_places[0]
#     lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
#     return lat, lon
#
#
# if __name__ == '__main__':
#     apikey = 'e9d96ce6-6d3b-4d62-9114-2185b11c9b8a'
#
#     con = sqlite3.connect('db.sqlite')
#     cur = con.cursor()
#
#     flats = get_flats_data_from_db(cur)
#     coords_dict = {}
#     keys = list(flats.keys())
#
#     for i in keys[600:801]:
#         coords = fetch_coordinates(apikey, flats[i]['address'])
#         coords_dict[i] = '; '.join(coords)
#     for i in coords_dict.keys():
#         cur.execute(f"""UPDATE flats SET coords='{coords_dict[i]}' WHERE flat_id={i}""")
#     con.commit()
#     con.close()
