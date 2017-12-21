
from django.core.management.base import BaseCommand
from wechathelper.models import WeatherTask, UserInfo



class Command(BaseCommand):
    '''
        向数据库添加数据
    '''


    def handle(self, *args, **options):
        self.add_weather_task()


    def add_weather_task(self):
        user = UserInfo()
        user.wechat_id =  '野猪妈妈和三个小野猪'
        user.user_name = '野猪妈妈和三个小野猪'
        user.city = '桂林'
        user.is_get_weather = True

        weather_task = WeatherTask()
        weather_task.user_name = '野猪妈妈和三个小野猪'
        weather_task.task_time_hour = 8
        weather_task.user_id = 0
        weather_task.task_time_minute = 0
        weather_task.save()
        user.save()
