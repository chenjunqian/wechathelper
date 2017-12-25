from django.db import models

# Create your models here.
class WeatherData(models.Model):
    '''
        天气数据模型
    '''
    date = models.IntegerField(default=None)
    city = models.CharField(max_length=30)
    shidu = models.CharField(max_length=30)
    pm25 = models.CharField(max_length=30)
    quality = models.CharField(max_length=30)
    wendu = models.IntegerField()
    notice = models.CharField(max_length=100)
 
class WeatherForecastData(models.Model):
    '''
        未来几天的天气情况
    '''
    relative_data = models.ForeignKey(WeatherData,on_delete=models.CASCADE)
    city = models.CharField(max_length=100, blank=True)
    date = models.IntegerField(default=None)
    high = models.CharField(max_length=100)
    low = models.CharField(max_length=100)
    fengli = models.CharField(max_length=100)
    weather_type = models.CharField(max_length=100)
    notice = models.CharField(max_length=100)


class UserInfo(models.Model):
    '''
        用户信息，主要存储用户的城市，接受哪些服务等
    '''
    wechat_id = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    is_get_weather = models.BooleanField(default=True)
    no_need_service = models.BooleanField(default=False)


class WeatherTask(models.Model):
    '''
        用户的天气定时任务
    '''
    created_time = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField(default=None)
    user_name = models.CharField(max_length=100)
    task_time_minute = models.IntegerField(default=None)
    task_time_hour = models.IntegerField(default=None)

