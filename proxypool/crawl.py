import re
from utils import get_page


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self,callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理：', proxy)
            proxies.append(proxy)
        return proxies


    def crawl_daili66(self):
        start_url = 'http://www.66ip.cn/nmtq.php?getnum=&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=0&proxytype=2&api=66ip'
        print('Crawling daili66 ips:')
        r = get_page(start_url)
        if r:
            text = r
            ips = re.findall('(\d+\..*?:\d+)',text)
            for ip in ips:
                yield ip

    def crawl_ip3366(self):
        for i in range(1,3):
            start_url = 'http://www.ip3366.net/free/?stype=1&page={}.format(i)'
            print('Crawling ip3366 ips:')
            html = get_page(start_url)
            ips = re.findall('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>', html)
            for ip, port in ips:
                proxy = ip+':'+port
                yield proxy

    def crawl_ips(self):
        start_url = 'http://118.24.52.95:5010/get_all/'
        print('test proxypool ips:')
        r = get_page(start_url)
        if r:
            text = r
            ips = re.findall('(\d+\..*?:\d+)',text)
            for ip in ips:
                yield ip
