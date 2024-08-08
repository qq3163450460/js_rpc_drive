#!/usr/bin/env python
# -*-coding:utf-8-*-
# date: 2024-01-25 15:01
# data: qq3163450460
import json
import time
import os
import subprocess
import psutil
from DrissionPage import ChromiumPage, ChromiumOptions
from config import URL, JS_PATHS, PORT, KEY, BROWSER_PATH, COOKIES, ON_OFF,USER_DATA_PATH
from loguru import logger
from flask import Flask, request

"""
"""
# logger.remove(handler_id=None)  # 禁用控制台日志输出
# 配置
if not os.path.exists('logs'):
    os.makedirs('logs')
logger.add("logs/rpc_drive.log",  # log文件地址
           level="DEBUG",  # log记录最低级别
           rotation="00:00",  # 将日志记录以大小、时间等方式进行分割或划分
           retention="3 days",  # 文件保留时间
           compression="zip",  # 文件压缩格式
           backtrace=True,
           # rotation="1 MB"  # 滚动大日志文件
           )


def kill_port(port):
    port_pid = {}
    for i in psutil.net_connections():
        pid = i.pid
        port_ = i.laddr.port
        port_pid[port_] = pid
    # 关闭占用端口的pid
    if port_pid.get(int(port)):
        find_kill = 'taskkill -f -pid %s' % port_pid[int(port)]
        subprocess.Popen(find_kill)
        logger.info(f'端口关闭成功:{port}')


class ChromeDrive:
    def __init__(self):
        self.start = True
        self.addr_or_opts = PORT + 1
        self.page = self.init_page()
        self.execute_js()

    def get_co(self):
        co = ChromiumOptions()
        co.set_paths(browser_path=BROWSER_PATH, user_data_path=USER_DATA_PATH)
        co.set_local_port(self.addr_or_opts)
        co.headless(on_off=ON_OFF)
        return co

    def init_page(self):
        # self.addr_or_opts += 1
        co = self.get_co()
        page = ChromiumPage(addr_or_opts=co, timeout=15)
        if COOKIES:
            page.set.cookies(cookies=COOKIES)
        page.get(URL)
        return page

    def int_chrome(self):
        if self.start is False:
            logger.error('浏览器已经在重启了')
            return ''
        self.start = False
        logger.info('浏览器异常开始重启....')
        kill_port(self.addr_or_opts)
        self.page.quit()
        time.sleep(1)
        self.page = self.init_page()
        time.sleep(1)
        logger.info('浏览器重启完成')
        self.execute_js()
        self.start = True

    def run_js_loaded(self, js_code):
        """
        执行js
        :param js_code:
        :return:
        """
        try:
            self.page.run_js_loaded(script=js_code, as_expr=True, timeout=30)
            return True
        except Exception as e:
            if '与页面的连接已断开' in str(e):
                self.int_chrome()
            logger.error(e)
            return False

    def execute_js(self):
        """
        执行文件夹所有js
        :return:
        """
        # paths = JS_PATHS()
        for js_path in JS_PATHS:
            with open(js_path, 'r', encoding='utf-8') as p:
                res = self.run_js_loaded(p.read())
                if res:
                    logger.debug(f'文件执行成功 ({js_path})')
                else:
                    logger.error(f'js文件执行失败 ({js_path})')
        logger.info('全部js执行完成')

    def eval_js(self, js_code):
        """
        执行js 获取返回结果
        :param js_code:
        :return:
        """
        try:
            res = self.page.run_js(script=js_code, as_expr=True, timeout=30)
            return json.dumps({'code': 0, 'data': res, 'msg': '操作成功'}, ensure_ascii=False)
        except Exception as e:
            if '与页面的连接已断开' in str(e):
                self.int_chrome()
            else:
                self.execute_js()
            logger.error(e)
            return json.dumps({'code': -1, 'msg': str(e), 'data': {}}, ensure_ascii=False)


app = Flask(__name__)

chrome_drive = ChromeDrive()


def dic_to_tuple(dic: dict):
    dic_list = sorted(dic, key=lambda x: x.split('_')[0])
    res = ()
    for key in dic_list:
        value = dic[key]
        type_ = key.split('_')[-1]
        if type_ == 'dict':
            value = json.loads(value)
        elif type_ == 'int':
            value = int(value)
        elif type_ == 'float':
            value = float(value)
        res += (value,)
    return res


@app.route('/eval_js/<fun_name>', methods=['POST', 'GET'])
def start(fun_name):
    if '.' in fun_name or chrome_drive.start is False:
        return json.dumps({'code': -1, 'msg': '异常连接', 'data': {}}, ensure_ascii=False), 500
    params = request.values.to_dict()
    str_params = dic_to_tuple(params)
    js_code = f"window.{fun_name}{str(str_params)}"
    logger.info(js_code)
    res = chrome_drive.eval_js(js_code=js_code)
    return res


@app.route('/ini_js', methods=['GET'])
def ini_js():
    key = request.values.get('key', None)
    if key == KEY:
        chrome_drive.init_page()
        chrome_drive.execute_js()
        return json.dumps({'code': 0, 'msg': '操作成功', 'data': JS_PATHS}, ensure_ascii=False)
    else:
        return json.dumps({'code': -1, 'msg': '密钥错误 刷新失败', 'data': {}}, ensure_ascii=False)


@app.errorhandler(Exception)
def error(e):
    return json.dumps({'code': -1, 'msg': str(e)}, ensure_ascii=False)


# 传输类型 str dict int float
#  http://127.0.0.1:8082/ini_js?key=xddmmm
if __name__ == '__main__':
    # ChromeDrive()
    app.run('0.0.0.0', port=PORT)
