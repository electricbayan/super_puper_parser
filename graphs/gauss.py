import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity
from scipy.interpolate import make_interp_spline
from matplotlib.ticker import FuncFormatter
from database_functions import get_flats_data_from_db


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

apartment_data = get_flats_data_from_db(cur)

plot_price_distribution(apartment_data)
