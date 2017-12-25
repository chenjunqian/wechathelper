
import json
import time
import datetime
import logging
import requests
from django.core.management.base import BaseCommand
from wechathelper.models import WeatherData, WeatherForecastData, UserInfo



class Command(BaseCommand):
    '''
        向数据库添加数据
    '''


    def handle(self, *args, **options):
        # self.add_weather_task()
        cities = ('桂林','上海')
        for city in cities:
            self.add_weather_data(city)
            time.sleep(5)


    def add_weather_task(self):
        user = UserInfo()
        user.wechat_id =  '野猪妈妈和三个小野猪'
        user.user_name = '野猪妈妈和三个小野猪'
        user.city = '上海'
        user.is_get_weather = True

        # weather_task = WeatherTask()
        # weather_task.user_name = '野猪妈妈和三个小野猪'
        # weather_task.task_time_hour = 8
        # weather_task.user_id = 0
        # weather_task.task_time_minute = 0
        # weather_task.save()
        user.save()

    def add_weather_data(self, city_name):
        weather_api_url = 'http://www.sojson.com/open/api/weather/json.shtml?city='
        response = requests.get(weather_api_url+str(city_name))
        if response.status_code == 200:
            json_response = json.loads(response.text)
            weather_data = json_response['data']
            forecast = weather_data['forecast']
            tomorrow_data = forecast[0]
            date = time.mktime(
                datetime.datetime.strptime(
                    json_response['date'],
                    "%Y%m%d").timetuple()
                )
            try:
                try_data = WeatherData.objects.filter(date=date, city=city_name)[0]
            except (WeatherData.DoesNotExist, IndexError) as e:
                try_data=None
            
            if try_data is not None:
                return

            weather_data = WeatherData(
                date = date,
                city = city_name,
                shidu = weather_data['shidu'],
                pm25 = weather_data['pm25'],
                quality = weather_data['quality'],
                wendu = weather_data['wendu'],
                notice = weather_data['ganmao']
            )

            weather_data.save()

            day = 0
            seconds_of_day = 86400
            for item in forecast:
                day = day + 1
                weather_forecast_data = WeatherForecastData(
                    relative_data = weather_data,
                    city = weather_data.city,
                    date = date + day*seconds_of_day,
                    high = item['high'],
                    low = item['low'],
                    fengli = item['fl'],
                    weather_type = item['type'],
                    notice = item['notice'],
                )

                weather_forecast_data.save()

            
