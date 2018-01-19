
import os, time, datetime
# from django.core.management.base import BaseCommand
# from django.db import connections
# from wechathelper.models import WeatherData, WeatherForecastData, UserInfo
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from bs4 import BeautifulSoup
import json
from multiprocessing.connection import Listener
import zmq
# from wxpy import *


# class Command(BaseCommand):
#     '''
#         向数据库添加数据
#     '''

#     def handle(self, *args, **options):
#         try:
#             user = UserInfo.objects.filter(
#                 user_name='野猪妈妈和三个小野猪'
#             ).order_by('-id')[0]
#             today_weather_data = WeatherData.objects.filter(city=user.city)
#         except UnicodeEncodeError as e:
#             print('error :'+'\n')
#             print(e)

#         for data in today_weather_data:
#             print('data :'+'\n')
#             print(data.date)
#             try:
#                 forecast_weather_data = WeatherForecastData.objects.filter(
#                     relative_data=data
#                 ).order_by('id')
#                 for item in forecast_weather_data:
#                     print('forecast_weather_data :'+'\n')
#                     print(item.date)
#             except Exception as e:
#                 print('error :'+'\n')
#                 print(e)

def crawl_singapore_weather_info():
    
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 '+
                    '(Linux; Android 6.0; Nexus 5 Build/MRA58N)'+
                    ' AppleWebKit/537.36 (KHTML, like Gecko)'+
                    ' Chrome/57.0.2950.4 Mobile Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Pragma': "no-cache",
    }

    url = 'http://www.weather.com.cn/weather/104010100.shtml'
    response = requests.get(
        url,
        headers=HEADERS
    )
    # print(response.text)
    soup = BeautifulSoup(response.text,'html.parser')
    weather_list = soup.find_all(
        'ul',
        class_='t clearfix'
    )

    weather_items = weather_list[0].find_all(
        'li'
    )
    day = -1
    for item in weather_items:
        day = day + 1
        if day == 0:
            wendu = item.find(
                'p',
                class_='tem'
            ).find('i').string
            print(wendu)
        else:
            high = item.find('p', class_='tem').find('span').string
            low = item.find('p', class_='tem').find('i').string
            fengli = item.find('p', class_='win').find('i').string
            weather_type = item.find('p', class_='wea').string
            print(high,low,fengli,weather_type)
        


if __name__ == '__main__':
    
    # context = zmq.Context()
    # socket = context.socket(zmq.REP)
    # socket.bind("tcp://127.0.0.1:6000")
    # while True:
    #     #  Wait for next request from client
    #     message = socket.recv()
    #     print("Received request: %s" % message)
    #     socket.send(b"World")

    crawl_singapore_weather_info()
                    


