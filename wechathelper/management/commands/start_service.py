
import os
import json
import time
import datetime
import logging
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management.base import BaseCommand
from wechathelper.models import WeatherData, WeatherForecastData, UserInfo
from wxpy import *

class Command(BaseCommand):
    '''
        开启服务使用的命令脚本
    '''

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler({
            'apscheduler.executors.default': {
                'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
                'max_workers': '20'
            },
            'apscheduler.executors.processpool': {
                'type': 'processpool',
                'max_workers': '5'
            },
            'apscheduler.timezone': 'Asia/Shanghai',
        })
        weather = Weather()
        wechat_bot = Bot(
            console_qr=-1,
            cache_path=True
        )
        wechat_bot.self.send('bot is on...')

        scheduler.add_job(
            weather.run_my_family_server,
            trigger='cron',
            day_of_week='1-7',
            hour='7',
            id='crawl_weather_info'
        )

        scheduler.add_job(
            weather.send_messege,
            args=[wechat_bot],
            trigger='cron',
            day_of_week='1-7',
            hour=8,
            id='my_test_job'
        )

        scheduler.start()

        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

        try:
            while True:
                time.sleep(1000)
        except(KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
            print(' Exit The Job!')


class Weather(object):
    '''
        关于天气信息的类
    '''
    def __init__(self):
        self.logger = logging.getLogger('djangosite.wechathelper.servive')
        self.weather_data = dict
        self.forecast = list
        self.tomorrow_data = dict
        self.date = int

    def crawl_weather_info(self, city_name):
        '''
            爬取天气信息
        '''
        weather_api_url = 'http://www.sojson.com/open/api/weather/json.shtml?city='
        response = requests.get(weather_api_url+str(city_name))
        if response.status_code == 200:
            json_response = json.loads(response.text)
            self.weather_data = json_response['data']
            self.forecast = self.weather_data['forecast']
            self.tomorrow_data = self.forecast[0]
            self.date = time.mktime(
                datetime.datetime.strptime(
                    json_response['date'],
                    "%Y%m%d").timetuple()
                )
            print(self.date)
            weather_data = WeatherData(
                date = self.date,
                city = city_name,
                shidu = self.weather_data['shidu'],
                pm25 = self.weather_data['pm25'],
                quality = self.weather_data['quality'],
                wendu = self.weather_data['wendu'],
                notice = self.weather_data['ganmao']
            )
            weather_data.save()

            day = 0
            seconds_of_day = 86400
            for item in self.forecast:
                day = day + 1
                weather_forecast_data = WeatherForecastData(
                    relative_data = weather_data,
                    date = self.date + day*seconds_of_day,
                    high = item['high'],
                    low = item['low'],
                    fengli = item['fl'],
                    weather_type = item['type'],
                    notice = item['notice'],
                )

                weather_forecast_data.save()

        else:
            self.logger.error(str(response.status_code))
            self.crawl_weather_info(city_name)

    def run(self):
        user_city_list = list(UserInfo.objects.values_list('city',flat=True).distinct())
        for use_city in user_city_list:
            self.logger.info(use_city)
            self.crawl_weather_info(use_city)

    # def qr_code_callback(self,uuid, status, qrcode):
    #     print(
    #         'uuid : '+str(uuid)+'\n'
    #         +'status : '+str(status)+'\n'
    #         +'qrcode : '+str(type(qrcode))+'\n'
    #     )   

    def run_my_family_server(self):
        self.crawl_weather_info('桂林')
        self.crawl_weather_info('上海')
        self.logger.info('crawl weather info success ! ')

    def send_messege(self, wechat_bot):
        wechat_bot.self.send('now is the time !!!')


