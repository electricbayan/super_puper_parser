import requests
import sqlite3
con = sqlite3.connect('db.sqlite')
cur = con.cursor()
d = {}
cooooooooooooooooords={}

for i in cur.execute("""SELECT * FROM flats"""):
    d[i[0]] = dict()
    d[i[0]]['price'] = i[1]
    d[i[0]]['address'] = i[3]
    d[i[0]]['total_square'] = i[5]
    d[i[0]]['living_square'] = i[6]
    d[i[0]]['type'] = i[7]

# for i in d.keys():
#     f.append(d[i]['address'])
import sqlite3
def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat
apikey = '2f7256a0-bdd3-43e5-9814-c1cb0b63e6af'
for i in d.keys():
    coords = fetch_coordinates(apikey, d[i]['address'])
    cooooooooooooooooords[i]='; '.join(coords)

for i in cooooooooooooooooords.keys()[:800]:
    cur.execute(f"""INSERT INTO flats(coords) VALUES('{cooooooooooooooooords[i]}')""")
con.commit()
con.close()


