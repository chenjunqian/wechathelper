
import os, time, datetime
# from django.core.management.base import BaseCommand
# from django.db import connections
# from wechathelper.models import WeatherData, WeatherForecastData, UserInfo
# from apscheduler.schedulers.background import BackgroundScheduler
import requests
from bs4 import BeautifulSoup
import json
import re
# from wxpy import *


# class Command(BaseCommand):
#     '''
#         测试数据
#     '''

#     def handle(self, *args, **options):
#         users = UserInfo.objects.filter(
#             user_name='野猪妈妈和三个小野猪'
#         ).order_by('-id')

#         for user in users:
#             today_weather_data = WeatherData.objects.filter(
#                 city=user.city
#             ).order_by('-id')[0]

#             forecast_weather_data = WeatherForecastData.objects.filter(
#                 date=today_weather_data.date,
#                 city=today_weather_data.city
#             ).order_by('-id')[0]

#             with open('test.txt','a') as file:
#                 file.write(forecast_weather_data.weather_type)

# if __name__ == '__main__':
    
    # context = zmq.Context()
    # socket = context.socket(zmq.REP)
    # socket.bind("tcp://127.0.0.1:6000")
    # while True:
    #     #  Wait for next request from client
    #     message = socket.recv()
    #     print("Received request: %s" % message)
    #     socket.send(b"World")

