#!/usr/bin/env python
# -*-coding:utf-8-*-
# date: 2024-01-25 16:13
# data:qq3163450460
#  (0,1,8,"{params}","{data}","{ua}")
import requests
from threading import Thread
import time


def run():
    data = {
        '1_str': 'params',
        '2_str': 'data',
        '3_str': 'ua'
    }
    # 传输类型 str dict int float
    url = 'http://127.0.0.1:8082/eval_js/get_a_b'
    res = requests.get(url=url, params=data)
    print(res.url)
    print(res.text)


# 'http://127.0.0.1:8082/eval_js/profileData'

def thread_run():
    t = time.time()
    a = []
    for i in range(100):
        dd = Thread(target=run)
        a.append(dd)
        dd.start()
        # break

    for i in a:
        i.join()

    print('耗时:', time.time() - t)


if __name__ == '__main__':
    run()
