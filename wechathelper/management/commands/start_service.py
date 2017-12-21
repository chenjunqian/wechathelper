
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
            hour=7,
            minute=30,
            id='crawl_weather_info'
        )

        scheduler.add_job(
            weather.send_messege,
            args=[wechat_bot],
            trigger='cron',
            hour=8,
            minute=00,
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
            try:
                try_data = WeatherData.objects.filter(date=self.date)[0]
            except (WeatherData.DoesNotExist, IndexError) as e:
                try_data=None
                self.logger.info(e)
            
            if try_data is not None:
                self.logger.info('The data is exist')
                return

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

    def run_my_family_server(self):
        cities = ('桂林','上海')
        for city in cities:
            self.crawl_weather_info(city)
            time.sleep(5)
        self.logger.info('crawl weather info success ! ')

    def send_messege(self, wechat_bot):
        wechat_bot.self.send('start to send weather info !!')
        try:
            family_group = wechat_bot.groups().search('野猪妈妈')[0]
        except IndexError:
            wechat_bot.self.send(str(IndexError))
            return
        
        user = UserInfo.objects.filter(is_get_weather=1).order_by('-id')[0]
        today_weather_data = WeatherData.objects.filter(city=user.city).order_by('-id')[0]
        forecast_weather_data = WeatherForecastData.objects.filter(date=today_weather_data.date).order_by('-id')[0]
        family_group.send(
            '今天天气预报 : \n'
            +str(today_weather_data.city)+'\n'
            +str(forecast_weather_data.weather_type)+'\n'
            +'温度 : '+str(today_weather_data.wendu)+'\n'
            +'湿度 : '+str(today_weather_data.shidu)+'\n'
            +'pm25 : '+str(today_weather_data.pm25)+'\n'
            +'空气质量 : '+str(today_weather_data.quality)+'\n'
            +'温馨提示 : '+str(forecast_weather_data.notice)
        )

    def format_ascii_str(self, string):
        re_str = ''.join(str(string)).encode('utf-8').strip()
        return re_str


