import sqlite3
import matplotlib.pyplot as plt
from database_functions import get_flats_data_from_db


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
