
import json
import time
import datetime
import logging
import requests
from wechathelper.models import WeatherData, WeatherForecastData

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
        response = requests.get(weather_api_url+str(city_name)).text
        if response.status_code == 200:
            json_response = json.loads(response)
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
            # weather_data.save()

            day = 0
            seconds_of_day = 86400
            for item in self.forecast
                day = day + 1
                weather_forecast_data = WeatherForecastData(
                    relative_data = weather_data,
                    date = self.date + day*seconds_of_day
                    high = item['high']
                    low = item['low']
                    fengli = item['fl']
                    weather_type = item['type']
                    notice = item['notice']
                )

        else:
            self.logger.error(str(response.status_code))
            self.crawl_weather_info(city_name)
            





if __name__ == '__main__':
    weather = Weather()
    weather.crawl_weather_info('桂林')
    print(weather.tomorrow_data)

