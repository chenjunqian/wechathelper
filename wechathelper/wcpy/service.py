import requests
import json
import time
import datetime

class Weather(object):
    '''
        关于天气信息的类
    '''
    def __init__(self):
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




if __name__ == '__main__':
    weather = Weather()
    weather.crawl_weather_info('桂林')
    print(weather.tomorrow_data)

