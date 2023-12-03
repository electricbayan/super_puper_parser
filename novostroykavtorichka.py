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


def plot_type_distribution_by_district(flats_data):
    districts = set(flat['district'] for flat in flats_data.values())

    type_counts = {district: {'Новостройка': 0, 'Вторичка': 0} for district in districts}

    for flat in flats_data.values():
        district = flat['district']
        if flat['type'] == 'Новостройка':
            type_counts[district]['Новостройка'] += 1
        elif flat['type'] == 'Вторичка':
            type_counts[district]['Вторичка'] += 1

    sorted_districts = sorted(districts)

    new_building_counts = [type_counts[district]['Новостройка'] for district in sorted_districts]
    secondary_market_counts = [type_counts[district]['Вторичка'] for district in sorted_districts]

    plt.figure(figsize=(12, 6))

    bar_width = 0.35
    index = range(len(sorted_districts))
    plt.bar(index, new_building_counts, width=bar_width, label='Новостройка')
    plt.bar([i + bar_width for i in index], secondary_market_counts, width=bar_width, label='Вторичка')

    plt.title('Распределение новостроек и вторичного жилья по районам')
    plt.xlabel('Район')
    plt.ylabel('Количество квартир')
    plt.xticks([i + bar_width / 2 for i in index], sorted_districts, rotation=45, ha="right")

    plt.legend()
    plt.show()


con = sqlite3.connect('db.sqlite')
cur = con.cursor()

flats_data = get_flats_data_from_db(cur)

plot_type_distribution_by_district(flats_data)
