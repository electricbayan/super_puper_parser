import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity
from scipy.interpolate import make_interp_spline
from matplotlib.ticker import FuncFormatter
from database_functions import get_flats_data_from_db
import os


def plot_price_distribution(apartments):
    prices = [apartment['price'] / 1e6 for apartment in apartments.values() if apartment['price'] <= 20e6]

    kde = KernelDensity(bandwidth=1.0, kernel='gaussian')
    kde.fit(np.array(prices).reshape(-1, 1))
    x_values = np.linspace(0, 10, 500)
    y_values = np.exp(kde.score_samples(x_values.reshape(-1, 1)))

    x_smooth = np.linspace(x_values.min(), x_values.max(), 200)
    spl = make_interp_spline(x_values, y_values, k=7)
    y_smooth = spl(x_smooth)

    bins = np.arange(0, 20.5, 1)
    n, _ = np.histogram(prices, bins=bins)
    plt.plot(bins[:-1], n, x_smooth, y_smooth, linestyle='-')

    plt.title('Распределение Цен на Квартиры')
    plt.xlabel('Цена (в миллионах)')
    plt.ylabel('Количество квартир')

    # Форматирование меток для отображения в миллионах
    formatter = FuncFormatter(lambda x, _: f'{x:.1f}M')
    plt.gca().xaxis.set_major_formatter(formatter)

    plt.show()


con = sqlite3.connect(os.path.dirname(os.getcwd()) + "\\db.sqlite")
cur = con.cursor()

apartment_data = get_flats_data_from_db(con)

plot_price_distribution(apartment_data)
