# -*- coding:utf-8 -*-

# import Download
# import qUrlManager
# import common
# import plugin
# import outputer
from lib.core import Download
from lib.core import qUrlManager
from lib.core import common
import threading
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from lib.core import plugin
from lib.core import outputer
output = outputer.outputer()




class SpiderMain(object):
    def __init__(self, root, threadNum):
        self.urls = qUrlManager.UrlManager()
        self.downloader = Download.Download()
        self.root = root
        self.threadNum = threadNum

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
            for i in list(range(self.threadNum)):
                if self.urls.has_new_url() is False:
                    break
                new_url = self.urls.get_new_url()

                print("craw:" + new_url)
                output.add_list("path_craw", new_url)
                output.build_html(common.qurlparse(self.root))
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
                disallow = ["sqlcheck"]
                _plugin = plugin.spiderplus("script", disallow)
                _plugin.work(_str["url"], _str["html"])
                self.urls.add_new_urls(new_urls)
root="http://www.baidu.com"
t=10
w8 = SpiderMain(root, t)
w8.craw()