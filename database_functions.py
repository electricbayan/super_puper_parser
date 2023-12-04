def get_flats_data_from_db(connect) -> dict:
    """
    Функция для получения словаря из базы данных flats
    Возвращает словарь формата:
    {flat_id: {price: int, address: str, total_square: float, living_square: float, type: str, district: str,
    coords: str, shops_nearby: int}}
    """
    cursor = connect.cursor()
    d = {}
    for string in cursor.execute("""SELECT * FROM flats"""):
        d[string[0]] = {}
        d[string[0]]['price'] = int(string[1])
        d[string[0]]['address'] = string[3]
        d[string[0]]['total_square'] = float(string[5])
        d[string[0]]['living_square'] = float(string[6])
        d[string[0]]['type'] = string[7]
        d[string[0]]['district'] = string[3].split(', ')[2]
        d[string[0]]['coords'] = string[8].replace(';', ',')
        d[string[0]]['shops_nearby'] = int(string[9])

    return d


def get_shops_data_from_db(connect) -> dict:
    """
        Функция для получения словаря из базы данных shops
        Возвращает словарь формата:
        {address: {coords: str, type: str}}
        """
    cursor = connect.cursor()
    d = {}
    for string in cursor.execute("""SELECT * FROM shops"""):
        d[string[0]] = {}
        d[string[0]]['coords'] = string[1]
        d[string[0]]['type'] = string[2]

    return d
