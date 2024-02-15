"""
REQUESTS AND DATA PREPARATION
"""

import requests
from PyQt6.QtGui import QPixmap

import configparser
config = configparser.ConfigParser()
config.read('config.ini')


class OofError(Exception):
    pass


def ip_request():
    params = {'apiKey': config['ip_api']['ip_api_key']}
    response = requests.get(config['ip_api']['ip_api_url'], params=params).json()
    return response['city'], [response['latitude'], response['longitude']]


def weather_request():
    params = {'key': config['weather_api']['weather_api_key'], 'q': city, 'days': 3}
    response_cur = requests.get(config['weather_api']['weather_url_current'], params=params).json()
    response_for = requests.get(config['weather_api']['weather_url_forecast'], params=params).json()
    return response_cur['current'], response_for['forecast']['forecastday']


def icon_request(url):
    pix = QPixmap()
    url = 'http:' + url
    response = requests.get(url)
    pix.loadFromData(response.content)
    return pix


def weather_data(param, forecast_index=0):
    data = weather_request()  # [0] [0] current [1] forecast(3 days) [1] [0-2] forecast for specified day
    if param == 'current':  # packing order: [0] icon_link [1] temp_c [2] last_updated
        icon_url = data[0]['condition']['icon']
        data_cur = [icon_url,
                    str(data[0]['temp_c']),
                    data[0]['last_updated']]
        return data_cur
    elif param == 'forecast' and 0 <= forecast_index <= 2:  # packing order: [[0] date [1] temp_max [2] temp_min
        date = data[1][forecast_index]['date'].split('-')
        date = '.'.join(date[::-1])  # yyyy-mm-dd -> dd.mm.yyyy
        data_forecast = [date,
                         str(data[1][forecast_index]['day']['maxtemp_c']),
                         str(data[1][forecast_index]['day']['mintemp_c'])]
        return data_forecast

    if param == 'forecast' and 0 <= forecast_index <= 2:
        print('forc', forecast_index)
        return forecast_data(forecast_index)
    else:
        raise OofError('wrong args in weather_data()')


city, coords = ip_request()  # [0] city [1] coords
