# import requests
# import sqlite3
# con = sqlite3.connect('db.sqlite')
# cur = con.cursor()
# d = {}
# cooooooooooooooooords={}
#
# for i in cur.execute("""SELECT * FROM flats"""):
#     d[i[0]] = dict()
#     d[i[0]]['price'] = i[1]
#     d[i[0]]['address'] = i[3]
#     d[i[0]]['total_square'] = i[5]
#     d[i[0]]['living_square'] = i[6]
#     d[i[0]]['type'] = i[7]
#
# # for i in d.keys():
# #     f.append(d[i]['address'])
# import sqlite3
# def fetch_coordinates(apikey, address):
#     base_url = "https://geocode-maps.yandex.ru/1.x"
#     response = requests.get(base_url, params={
#         "geocode": address,
#         "apikey": apikey,
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
#     return lon, lat
# apikey = '2f7256a0-bdd3-43e5-9814-c1cb0b63e6af'
# for i in d.keys():
#     coords = fetch_coordinates(apikey, d[i]['address'])
#     cooooooooooooooooords[i]='; '.join(coords)
#
# for i in cooooooooooooooooords.keys()[:800]:
#     cur.execute(f"""INSERT INTO flats(coords) VALUES('{cooooooooooooooooords[i]}')""")
# con.commit()
# con.close()
#
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d

con = sqlite3.connect('db.sqlite')
cur = con.cursor()
d = {}

for i in cur.execute("""SELECT * FROM flats"""):
    d[i[0]] = dict()
    d[i[0]]['price'] = int(i[1])
    d[i[0]]['address'] = i[3]
    d[i[0]]['total_square'] = float(i[5])
    d[i[0]]['living_square'] = float(i[6])
    d[i[0]]['type'] = i[7]
    d[i[0]]['district'] = i[3].split(', ')[2]

district_data = {}
for i in d.keys():
    district = d[i]['district']
    if district not in district_data:
        district_data[district] = {'prices': [], 'l_squares': [], 't_squares': []}
    district_data[district]['prices'].append(d[i]['price'])
    district_data[district]['l_squares'].append(d[i]['living_square'])
    district_data[district]['t_squares'].append(d[i]['total_square'])

avg_prices = [np.mean(data['prices']) / 1e6 for data in district_data.values()]
avg_price_per_sqm = [
    (np.mean(data['prices']) / np.mean(data['l_squares']) / 1e3) if data['l_squares'] else 0
    for data in district_data.values()
]
avg_t_squares = [np.mean(data['t_squares']) for data in district_data.values()]
districts = list(district_data.keys())

fig, axes = plt.subplots(1, 3, figsize=(12, 4))

axes[0].bar(districts, avg_prices, color='blue')
axes[0].set_title('Средние Цены (млн)')
axes[0].tick_params(axis='x', rotation=90)

axes[1].bar(districts, avg_price_per_sqm, color='purple')
axes[1].set_title('Средняя Цена за кв. метр (тыс.)')
axes[1].tick_params(axis='x', rotation=90)

axes[2].bar(districts, avg_t_squares, color='orange')
axes[2].set_title('Средняя Общая Площадь')
axes[2].tick_params(axis='x', rotation=90)

plt.tight_layout()

plt.savefig('цены.png')
plt.savefig('цены за квадратный метр.png')
plt.savefig('средние площади.png')

plt.show()
