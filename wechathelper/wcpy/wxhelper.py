from wxpy import *

class WxHelper(object):
    '''
        微信接口的功能都在这个类里实现
    '''
    def __init__(self):
        self.instance_dict = dict()

    @property
    def instance_dict(self):
        '''
            储存微信实例的字典
        '''
        return self.instance_dict

    def add_new_instance(self, wxid, bot):
        '''
            向微信实例字典中添加新的实例
        '''
        if not wxid or not isinstance(bot, Bot):
            raise ValueError('wxid is empty')
        if not isinstance(bot, Bot):
           raise ValueError('%s is not wxpy.Bot type',bot.__name__) 
        else:
            self.instance_dict[wxid] = bot

