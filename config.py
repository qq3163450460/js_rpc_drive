#!/usr/bin/env python
# -*-coding:utf-8-*-
# date: 2024-01-25 15:01
# data:qq3163450460
import json
import os
import shutil
from urllib.parse import urlparse

file = os.path.dirname(__file__)


def get_js_paths():
    global file
    cmd_path = file + '/jsdata/'
    paths = os.listdir(cmd_path)
    js_paths = list()
    for path in paths:
        if path.endswith('.js'):
            js_paths.append(cmd_path + path)
    return js_paths


def remove_file(folder):
    if not os.path.exists(folder):
        return
    try:
        shutil.rmtree(folder)
    except OSError as e:
        print(e)


with open(f'{file}/config.json', 'r', encoding='utf-8-sig') as p:
    CONFIG = json.loads(p.read())

ON_OFF = CONFIG['ON_OFF']  # 是否无头 True无头
...
USER_DATA_PATH = f'{file}/{CONFIG["USER_DATA_PATH"]}'  # 浏览器缓存地址
remove_file(USER_DATA_PATH)  # 每次启动删除缓存文件夹
...
BROWSER_PATH = CONFIG['BROWSER_PATH']  # 浏览器地址
...
URL = CONFIG['URL']  # 需要打开的网站
...
COOKIES = CONFIG["COOKIES"]  # {'name1': 'value1', 'name2': 'value2'}
if COOKIES:
    host = urlparse(url=URL).hostname
    COOKIES['domain'] = host
...

PORT = 8082  # flask 端口
KEY = 'xddmmm'  # 在线刷新js的key
#  http://127.0.0.1:8082/ini_js?key=xddmmm

JS_PATHS = get_js_paths()  # 获取全部js文件名称
print(JS_PATHS)

# 传输类型 str dict int float
