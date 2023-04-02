# -*- coding:utf-8 -*-
# import Download
# import qUrlManager
# import common
# import plugin

import lib.Download as Download
import lib.qUrlManager as qUrlManager
from lib import common
from lib import plugin
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import threading
import queue



class SpiderMain(object):
    def __init__(self, root,result_queue):
        self.urls = qUrlManager.UrlManager()
        self.downloader = Download.Download()
        self.root = root
        self.result_queue=result_queue
    # 去重

    def _judge(self, domain, url):
        if url.find(domain) != -1:
            return True
        else:
            return False

    def _parse(self, page_url, content):
        if content is None:
            return
        soup = BeautifulSoup(content, 'html.parser')  # 创建对象
        _news = self._get_new_urls(page_url, soup)
        return _news

    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        links = soup.find_all('a')
        for link in links:
            new_url = link.get('href')
            new_full_url = urljoin(page_url, new_url)
            if self._judge(self.root, new_full_url):
                new_urls.add(new_full_url)
        return new_urls

    def craw(self):
        self.urls.add_new_url(self.root)
        while self.urls.has_new_url():
            _content = []
            th = []
            for i in list(range(5)):
                if self.urls.has_new_url() is False:
                    break
                new_url = self.urls.get_new_url()
                self.result_queue.put("craw:" + new_url)
                print("craw:" + new_url)
                # 多线程下载
                t = threading.Thread(target=self.downloader.download, args=(new_url, _content))
                t.start()
                th.append(t)
            for t in th:
                t.join()
            for _str in _content:
                if _str is None:
                    continue
                new_urls = self._parse(new_url, _str["html"])
                _plugin = plugin.spiderplus("script", [])
                _plugin.work(_str["url"], _str["html"],self.result_queue)                
                self.urls.add_new_urls(new_urls)
def url_scan(url,result_queue):
    if not url.startswith("http://"):
        url = "http://"+url
    x = SpiderMain(url,result_queue)
    x.craw()
# url="http://www.baidu.com"
# t = queue.Queue()
# url_scan(url=url,result_queue=t)
# x=[]
# while not t.empty():
#     q=t.get()
#     x.append(q)
# print(x)