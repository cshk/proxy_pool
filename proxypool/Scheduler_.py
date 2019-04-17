from multiprocessing import Process
from api_flask import app
from getter_ import Getter
from test import Tester
from settings import *
import time


class Scheduler(object):
    def tester(self, cycle=TESTER_CYCLE):
        tester = Tester()
        while True:
            print('定时测试开始运行...')
            tester.run()
            time.sleep(cycle)

    def getter(self, cycle=GETTER_CYCLE):
        getter = Getter()
        while True:
            print('开始抓取代理...')
            getter.run()
            time.sleep(cycle)

    def api(self):
        app.run(API_HOST,API_PORT)

    def run(self):
        print('-------------------多线程异步代理池开始运行-------------------')
        if TESTER_ENABLED:
            tester_process = Process(target=self.tester)
            tester_process.start()
        if GETTER_ENABLED:
            getter_process = Process(target=self.getter)
            getter_process.start()
        if API_ENABLED:
            api_process = Process(target=self.api)
            api_process.start()
