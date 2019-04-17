import asyncio
import aiohttp
import time
import sys
from aiohttp import ClientError
from aiohttp import ClientProxyConnectionError
from db import RedisClient
from settings import *


class Tester(object):
    def __init__(self):
        self.redis =RedisClient()

    async def single_proxy(self, proxy):
        async with aiohttp.ClientSession() as session:
            try:
                real_proxy = 'https://' + proxy
                print('正在测试:', proxy)
                async with session.get(TEST_URL, proxy=real_proxy,timeout=10,allow_redirects=False,verify_ssl=False) as resp:
                    if 200 == resp.status:
                        self.redis.max(proxy)
                    else:
                        self.redis.decrease(proxy)
                        print('请求错误:', resp.status, 'IP', proxy)

            except (ClientError, ClientProxyConnectionError,aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError,AttributeError):
                self.redis.decrease(proxy)
                print('代理请求失败', proxy)

    def run(self):
        print('开始检测ip:....')
        try:
            count = self.redis.count()
            print('当前剩余', count, '个代理')
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                end = min(i+BATCH_TEST_SIZE, count)
                print('正在测试第', start+1,'-',end, '个代理')
                test_proxies = self.redis.batch(start, end)
                loop = asyncio.get_event_loop()
                tasks = [self.single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            print('检测异常:', e.args)

# r = Tester()
# r.run()