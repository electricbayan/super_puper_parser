import sqlite3
import matplotlib.pyplot as plt
from database_functions import get_flats_data_from_db
import os


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


con = sqlite3.connect(os.path.dirname(os.getcwd()) + "\\db.sqlite")
cur = con.cursor()

flats_data = get_flats_data_from_db(con)

plot_type_distribution_by_district(flats_data)
