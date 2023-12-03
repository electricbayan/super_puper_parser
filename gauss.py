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
    prices = [apartment['price'] / 1e6 for apartment in apartments.values() if apartment['price'] <= 30e6]

    kde = KernelDensity(bandwidth=1.0, kernel='gaussian')
    kde.fit(np.array(prices).reshape(-1, 1))
    x_values = np.linspace(0, 30, 1000)
    y_values = np.exp(kde.score_samples(x_values.reshape(-1, 1)))

    x_smooth = np.linspace(x_values.min(), x_values.max(), 5000)
    spl = make_interp_spline(x_values, y_values, k=3)
    y_smooth = spl(x_smooth)

    plt.plot(x_smooth, y_smooth, 'r-')

    bins = np.arange(0, 30.5, 1)
    n, _ = np.histogram(prices, bins=bins)
    plt.plot(bins[:-1], n, linestyle='-')

    plt.title('Распределение Цен на Квартиры')
    plt.xlabel('Цена (в миллионах)')
    plt.ylabel('Количество квартир')

    # Форматирование меток для отображения в миллионах
    formatter = FuncFormatter(lambda x, _: f'{x:.1f}M')
    plt.gca().xaxis.set_major_formatter(formatter)

    plt.show()

con = sqlite3.connect('db.sqlite')
cur = con.cursor()

apartment_data = get_apartment_data_from_db(cur)

plot_price_distribution(apartment_data)
