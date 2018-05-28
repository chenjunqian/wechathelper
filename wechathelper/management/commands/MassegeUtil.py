import logging
import datetime
import time
from wechathelper.models import TextMessageTask

class MessageTask(object):

    def __init__(self):
        self.logger = logging.getLogger('djangosite.wechathelper.servive')
        

    def getTextMessageTaskQuerySetByTime(self, minute, hour):
        '''
            根据时间获取发送文本任务

            返回 QuerySet
        '''
        try:
            textMessageTasks = TextMessageTask.objects.filter(
                task_time_minute = minute,
                task_time_hour = hour,
                cancel_task = False
            )
        except (WeatherData.DoesNotExist, IndexError) as error:
            textMessageTasks=None
            self.logger.info(error)

        return textMessageTasks


    def getTextMessageTaskInfo(self, minute, hour):
        '''
            根据时间获取发送文本任务

            返回 任务信息 List
        '''
        textMessageTasks = self.getTextMessageTaskQuerySetByTime(minute,hour)
        info_list = list()
        for task in textMessageTasks:
            info_dict = dict()
            info_dict['to_user_name'] = task.to_user_name
            info_dict['to_user_id'] = task.to_user_id
            info_dict['message'] = task.message
            info_list.append(info_dict)

        return info_list

    def sendTaskMessage(self, wechat_bot):
        
        now = datetime.datetime.now()
        minute = now.minute
        hour = now.hour
        task_list = self.getTextMessageTaskInfo(minute, hour)
        
        for task in task_list:
            
            to_user_name = task['to_user_name']
            message = task['message']

            try:
                target_user = wechat_bot.friends().search(to_user_name)[0]
            except IndexError:
                wechat_bot.self.send(str(IndexError))
                return

            target_user.send(
                message
            )
        
        

            
