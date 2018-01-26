
import os, time, datetime
# from django.core.management.base import BaseCommand
# from django.db import connections
# from wechathelper.models import WeatherData, WeatherForecastData, UserInfo
# from apscheduler.schedulers.background import BackgroundScheduler
import requests
from bs4 import BeautifulSoup
import json
import re
# from wxpy import *


# class Command(BaseCommand):
#     '''
#         测试数据
#     '''

#     def handle(self, *args, **options):
#         users = UserInfo.objects.filter(
#             user_name='野猪妈妈和三个小野猪'
#         ).order_by('-id')

#         for user in users:
#             today_weather_data = WeatherData.objects.filter(
#                 city=user.city
#             ).order_by('-id')[0]

#             forecast_weather_data = WeatherForecastData.objects.filter(
#                 date=today_weather_data.date,
#                 city=today_weather_data.city
#             ).order_by('-id')[0]

#             with open('test.txt','a') as file:
#                 file.write(forecast_weather_data.weather_type)

if __name__ == '__main__':
    
    # context = zmq.Context()
    # socket = context.socket(zmq.REP)
    # socket.bind("tcp://127.0.0.1:6000")
    # while True:
    #     #  Wait for next request from client
    #     message = socket.recv()
    #     print("Received request: %s" % message)
    #     socket.send(b"World")
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 '+
                    '(Linux; Android 6.0; Nexus 5 Build/MRA58N)'+
                    ' AppleWebKit/537.36 (KHTML, like Gecko)'+
                    ' Chrome/57.0.2950.4 Mobile Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Pragma': "no-cache",
    }

    url = 'https://www.accuweather.com/en/se/orebro/314339/daily-weather-forecast/314339?day=1'
    response = requests.get(
        url,
        headers=HEADERS
    )

    response.encoding = 'UTF-8'
    soup = BeautifulSoup(response.text,'html.parser')
    feed_list = soup.find_all('div', class_='panel-list',)[1]

    weather_info_list = feed_list.find_all('div', class_='bg')

    today_weather_info = weather_info_list[0]

    wendu = today_weather_info.find('span', class_='large-temp').string.replace('°','')

    print('wendu : '+wendu)

    for weather_item in weather_info_list:
        try:
            low = weather_item.find('span', class_='small-temp').string
            low = low.replace('/','')
        except AttributeError as error:
            continue

        weather_type = weather_item.find('span', class_='cond').string
        high = weather_item.find('span', class_='large-temp').string

        print(weather_type)
        print(high)
        print(low)


