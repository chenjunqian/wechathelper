from wxpy import *
import datetime
import time
from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from wechathelper.models import WeatherData, WeatherForecastData, UserInfo, WeatherTask


class Command(BaseCommand):
    '''
        开启微信助手服务微信号
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
        wx_helper = WxHelper(scheduler)
        wx_helper.login()

class WxHelper(object):
    '''
        微信助手的功能都在这个类里实现
    '''
    def __init__(self, backgroundScheduler):
        self.instance_dict = dict()
        self.schediler = backgroundScheduler

    def login(self):
        '''
            登录微信，返回一个二维码
        '''
        self.wechat_helper = Bot()

    def send_weather_info(self):
        '''
            发送天气预报
        '''
        self.schediler.add_job(
            'weather.run',
            trigger='cron',
            minutes='0-59',
            id='crawl_weather_info'
        )

        current_minute = datetime.datetime.fromtimestamp(time.time()).strftime('%M')
        current_hour = datetime.datetime.fromtimestamp(time.time()).strftime('%H')
        weather_task_list = list(WeatherTask.objects.get(
            task_time_minute=int(current_minute),
            task_time_hour=int(current_hour)
            )

        for task in weather_task_list:
            print(task)

