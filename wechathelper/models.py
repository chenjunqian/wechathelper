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
    notice = models.CharField(max_length=30)
 
class WeatherForecastData(models.Model):
    relative_data = models.ForeignKey(WeatherData,on_delete=models.CASCADE)
    date = models.IntegerField(default=None)
    high = models.CharField(max_length=30)
    low = models.CharField(max_length=30)
    fengli = models.CharField(max_length=30)
    weather_type = models.CharField(max_length=30)
    notice = models.CharField(max_length=30)
