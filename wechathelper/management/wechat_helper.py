
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management.base import BaseCommand
from multiprocessing.connection import Listener
from wxpy import *


class Command(BaseCommand):
    '''
        开启微信服务使用的命令脚本
    '''

    def handle(self, *args, **options):
        self.init()


    def init(self):
        '''
            由于Command的__init__函数不方便使用，
            所以本类的参数初始化在此方法内
        '''
        self.wechats_dict = dict()
        self.address = ('localhost',6000)
        with Listener(self.address, authkey=b'use_wechat') as listener:
            with listener.accept() as conn:
                msg = conn.recv()
                


    def is_instance_exist(self, user_key):
        '''
            判断用户是否已经在服务器内登陆
        '''
        if user_key in self.wechats_dict:
            return True
        else:
            return False
        

    def login_wechat_instance(self):
        '''
            登陆微信实例，成返回True，失败返回False
        '''
        if not self.is_instance_exist(user_key):
            self.wechats_dict[user_key] = wechat_instance
            return True
        else:
            return False