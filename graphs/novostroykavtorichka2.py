import sqlite3
import matplotlib.pyplot as plt


def get_flats_data_from_db(cursor):
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

def create_bar_chart(data):
    district_shops = {}
    district_counts = {}

    for flat_id, flat_data in data.items():
        district = flat_data['district']
        shops_nearby = flat_data['shops_nearby']

        if district not in district_shops:
            district_shops[district] = 0
            district_counts[district] = 0

        district_shops[district] += shops_nearby
        district_counts[district] += 1

    district_averages = {district: district_shops[district] / district_counts[district] for district in district_shops}

    districts = list(district_averages.keys())
    averages = list(district_averages.values())

    plt.bar(districts, averages)
    plt.xlabel('Район')
    plt.ylabel('Среднее количество магазинов')
    plt.title('Среднее количество магазинов в районе')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

con = sqlite3.connect('db.sqlite')
cur = con.cursor()

flats_data = get_flats_data_from_db(cur)
create_bar_chart(flats_data)
