import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity
from scipy.interpolate import make_interp_spline
from matplotlib.ticker import FuncFormatter

def get_apartment_data_from_db(cursor):
    """
    Функция для извлечения данных из базы данных
    Возвращает словарь в формате:
    {apartment_id: {price: int, address: str, total_square: float, living_square: float, type: str, district: str}}
    """
    data = {}
    for row in cursor.execute("""SELECT * FROM flats"""):
        data[row[0]] = {}
        data[row[0]]['price'] = int(row[1])
        data[row[0]]['address'] = row[3]
        data[row[0]]['total_square'] = row[5]
        data[row[0]]['living_square'] = row[6]
        data[row[0]]['type'] = row[7]
        data[row[0]]['district'] = row[3].split(', ')[2]
    return data

def plot_price_distribution(apartments):
    prices = [apartment['price'] / 1e6 for apartment in apartments.values() if apartment['price'] <= 30e6]  # Фильтр цен до 30M

    # Ядерная оценка плотности для цен на квартиры
    kde = KernelDensity(bandwidth=1.0, kernel='gaussian')
    kde.fit(np.array(prices).reshape(-1, 1))
    x_values = np.linspace(0, 30, 1000)
    y_values = np.exp(kde.score_samples(x_values.reshape(-1, 1)))

    # Сглаживание линии с увеличением количества точек
    x_smooth = np.linspace(x_values.min(), x_values.max(), 5000)
    spl = make_interp_spline(x_values, y_values, k=3)
    y_smooth = spl(x_smooth)

    # Построение графика сглаженной линии цен на квартиры без точек
    plt.plot(x_smooth, y_smooth, 'r-')

    # Построение гистограммы цен на квартиры без точек
    bins = np.arange(0, 30.5, 1)  # Шаг 1M, максимальная цена 30M
    n, _ = np.histogram(prices, bins=bins)
    plt.plot(bins[:-1], n, linestyle='-')

    plt.title('Распределение Цен на Квартиры')
    plt.xlabel('Цена (в миллионах)')
    plt.ylabel('Количество квартир')

    # Форматирование меток для отображения в миллионах
    formatter = FuncFormatter(lambda x, _: f'{x:.1f}M')
    plt.gca().xaxis.set_major_formatter(formatter)

    plt.show()

# Подключение к базе данных SQLite
con = sqlite3.connect('db.sqlite')
cur = con.cursor()

# Извлечение данных о квартирах из базы данных
apartment_data = get_apartment_data_from_db(cur)

# Построение графика распределения цен с использованием ядерной оценки плотности (до 30M) без точек
plot_price_distribution(apartment_data)
