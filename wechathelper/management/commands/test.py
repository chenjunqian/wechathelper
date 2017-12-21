
import os, time, datetime
from django.core.management.base import BaseCommand
# from wechathelper.models import WeatherData, WeatherForecastData, UserInfo
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import json
from wxpy import *


class Command(BaseCommand):
    '''
        向数据库添加数据
    '''

    def handle(self, *args, **options):
        wechat_bot = Bot(
            console_qr=-1,
            cache_path=True
        )
        try:
            family_group = wechat_bot.groups().search('野猪妈妈')[0]
            family_group.send('测试一下')
        except IndexError:
            wechat_bot.self.send(str(IndexError))

        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

        try:
            while True:
                time.sleep(1000)
        except(KeyboardInterrupt, SystemExit):
            print(' Exit The Job!')



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

