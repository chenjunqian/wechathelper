
import os, time, datetime
from django.core.management.base import BaseCommand
from django.db import connections
from wechathelper.models import WeatherData, WeatherForecastData, UserInfo
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import json
from wxpy import *


class Command(BaseCommand):
    '''
        向数据库添加数据
    '''

    def handle(self, *args, **options):
        user = UserInfo.objects.filter(user_name='野猪妈妈和三个小野猪').order_by('-id')[0]
        today_weather_data = WeatherData.objects.filter(city=user.city)
        for data in today_weather_data:
            print('data :'+'\n')
            print(data.date)
            try:
                forecast_weather_data = WeatherForecastData.objects.filter(
                    # date=data.date,
                    relative_data=data
                ).order_by('id')
                for item in forecast_weather_data:
                    print('forecast_weather_data :'+'\n')
                    print(item.date)
            except IndexError as e:
                print('error :'+'\n')
                print(e)
            


# if __name__ == '__main__':
#     weather_api_url = 'http://www.sojson.com/open/api/weather/json.shtml?city='
#     cities = ('桂林','上海')
#     for city in cities:
#         print(city)
#         response = requests.get(weather_api_url+str(city))
#         if response.status_code == 200:
#             json_response = json.loads(response.text)
#             print(str(json_response))
#         else:
#             print('crawl fail...')
#         time.sleep(5)

