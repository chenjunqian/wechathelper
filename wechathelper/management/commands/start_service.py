
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management.base import BaseCommand
from WeatherUtil import Weather
from MassegeUtil import MessageTask
from wxpy import *

class Command(BaseCommand):
    '''
        开启家庭服务使用的命令脚本
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
            hour=6,
            minute=30,
            id='crawl_weather_info'
        )

        scheduler.add_job(
            weather.send_messege,
            args=[wechat_bot],
            trigger='cron',
            hour=7,
            minute=00,
            id='my_weather_job'
        )

        messageTask = MessageTask()
        scheduler.add_job(
            messageTask.sendTaskMessage(wechat_bot),
            trigger='interval',
            seconds=10,
            id='my_message_job'
        )

        scheduler.start()

        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

        try:
            while True:
                time.sleep(1000)
        except(KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
            print(' Exit The Job!')