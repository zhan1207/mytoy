import os
import re

import redis
import requests
from django.conf.global_settings import STATICFILES_DIRS
from lxml import etree
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSer
from .models import UserModel, Music
import hashlib


def get_unique_str(password):
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()


class RegView(APIView):
    def post(self, request):
        userdata = request.data
        if userdata['password'] != userdata['password1']:
            return Response({'code': 999, 'msg': '两次密码不一样'})
        userdict = {
            'username': userdata['username'],
            'password': get_unique_str(userdata['password']),
            'nickname': userdata['nickname'],
            'gender': userdata['gender'],
        }
        print(userdict)
        try:
            UserModel.objects.create(**userdict).save()
            return Response({'code': 200, 'msg': '注册成功'})
        except:
            return Response({'code': 100, 'msg': '注册失败'})


class LoginView(APIView):
    def post(self, request):
        data = request.data
        if UserModel.objects.filter(username=data['username'], password=get_unique_str(data['password'])).first():
            host = '192.168.99.100'  # docker内redis IP
            r = redis.Redis(host=host, port=6380)  # port端口号
            if r.set(data['username']) != None:
                res = {
                    'code': 401,
                    'message': '已经登录'
                }
                return Response(res)
            else:
                # 存入数据
                r.set('life', 'life')
                # 设置过期时间
                r.expire('life', 1296000)
            return Response({'code': 200, 'msg': '登录成功'})
        return Response({'code': 100, 'msg': '账号或密码错误'})


class Get_musicAPI(APIView):
    def get(self, request):
        url = 'http://www.9ku.com/erge/gushi.htm'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        }
        res = requests.get(url=url, headers=headers)
        tree = etree.HTML(res.text)

        # 分类路由
        # class_list = tree.xpath('//li/a/@href')
        # title__list = tree.xpath('//ol[@id="f0"]/li/a/text()')
        # 歌曲路由
        a_list = tree.xpath('//ol[@id="f0"]/li/a/@href')
        for a in a_list:
            a_href = "http://www.9ku.com" + a

            res1 = requests.get(url=a_href)
            tree1 = etree.HTML(res1.text)
            title_ = tree1.xpath('//div[@class="playingTit"]/h1/text()')[0]
            classify = tree1.xpath('//div[@class="playingTit"]/h2/a/text()')[0]
            src = re.findall(r"\d+", a_href)[1]
            url = 'http://mp3.9ku.com/m4a/%s.m4a' % src
            music_res = requests.get(url=url)
            musicname = f'{title_}.m4a'
            # with open(f'{musicname}', 'wb') as f:
            #     f.write(music_res.content)
            with open('static/music/' + musicname, 'wb') as f:
                f.write(music_res.content)
            music = {}
            music['title'] = title_
            music['musicurl'] = musicname
            music['source'] = '九酷音乐网'
            music['classify'] = classify
            music_model = Music.objects.create(
                musicname=title_,
                classify=classify,
                source='九酷音乐网',
                musicimage='',
                musicurl=musicname
            ).save()
        return Response({'code': 'ok'})
