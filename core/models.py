from django.db import models

# Create your models here.


class TimeStampedModel(models.Model):

    """ Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True)  # Model이 생성된 날짜
    updated = models.DateTimeField(auto_now=True)  # Model을 저장할 때마다 새로운 날짜로 업데이트

    class Meta:
        abstract = True  # 데이터베이스에 TimeStampedModel 등록하지 않을 때 사용
