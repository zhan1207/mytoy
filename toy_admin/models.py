from django.db import models
from datetime import datetime


# App用户表
class UserModel(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    phone = models.CharField(max_length=32,null=True)
    nickname = models.CharField(max_length=50)
    gender = models.CharField(max_length=10,default=1)  # 1 女 2男
    avatar = models.FileField(upload_to='static/avatar', null=True)
    createTime = models.TimeField(default=datetime.now())

    class Meta:
        db_table = 'user'


# Toy玩具表
class ToyModel(models.Model):
    devicekey = models.CharField(max_length=32)
    babyname = models.CharField(max_length=32, null=True)
    toyname = models.CharField(max_length=32, null=True)
    avatar = models.FileField(upload_to='static/avatar', null=True)
    createTime = models.TimeField(default=datetime.now())
    bindUser = models.IntegerField(default=0)

    class Meta:
        db_table = 'toy'

# 音乐
class Music(models.Model):
    musicname = models.CharField(max_length=52)
    classify = models.CharField(max_length=52)
    source = models.CharField(max_length=52)
    musicimage = models.CharField(max_length=255)
    musicurl = models.CharField(max_length=255)
    class Meta:
        db_table = 'music'