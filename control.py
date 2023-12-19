"""
REQUESTS AND DATA PREPARATION
"""
import requests
from PyQt6.QtGui import QPixmap

import config


def ip_request():
    params = {'apiKey': config.ip_api_key}
    response = requests.get(config.ip_url, params=params).json()
    return response['city']


def weather_request():
    params_cur = {'key': config.weather_api_key, 'q': city}
    params_for = {'key': config.weather_api_key, 'q': city, 'days': 3}
    response_cur = requests.get(config.weather_url_current, params=params_cur).json()
    response_for = requests.get(config.weather_url_forecast, params=params_for).json()
    return response_cur['current'], response_for['forecast']['forecastday']


def icon_request(link):
    pix = QPixmap()
    icon = requests.get('http:'+link)
    pix.loadFromData(icon.content)
    return pix


city = ip_request()  # [0] city
response_w = weather_request()  # [0] current [1] forecast(3 days) [1][0-2] forecast for the each day(insert index)


def current_data():  # packing order: [[0] icon_link [1] temp_c]
    data = response_w[0]
    data = [icon_request(data['condition']['icon']), str(data['temp_c'])]
    return data


def forecast_data(index):  # packing order: [[0] date [1] temp_max [2] temp_min]
    data = response_w[1][index]
    date = data['date'].split('-')
    date = '.'.join(date[::-1])  # yyyy-mm-dd -> dd.mm.yyyy
    data = [date, str(data['day']['maxtemp_c']), str(data['day']['mintemp_c'])]
    return data
