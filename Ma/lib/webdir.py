import os
import sys
import queue
import requests
import threading
from urllib.parse import urlparse

class webdir:
    def __init__(self, root,result_queue):
        self.result_queue=result_queue
        self.root = urlparse(root)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
            'Referer': 'http://www.shiyanlou.com',
            'Cookie': 'whoami=who',
        }
        self.task = queue.Queue()
        self.s_list = []

        filename = os.path.join(os.getcwd(), "data", "dir.txt")

        for line in open(filename):
            self.task.put(self.root.scheme+"://"+self.root.netloc + line.strip())

    def checkdir(self, url):
        status_code = 0
        try:
            r = requests.head(url, headers=self.headers)
            status_code = r.status_code
        except:
            status_code = 0
        return status_code

    def test_url(self):
        while not self.task.empty():
            url = self.task.get()
            s_code = self.checkdir(url)
            if s_code == 200:
                self.s_list.append(url)
            self.result_queue.put("Testing: %s status:%s"%(url, s_code))
            print("Testing: %s status:%s"%(url, s_code))


    def work(self):
        threads = []
        for i in range(5):
            t = threading.Thread(target=self.test_url())
            threads.append(t)
            t.start()
        for i in threads:
            t.join()
        self.result_queue.put('[*] The DirScan is complete!')
        print('[*] The DirScan is complete!')

    def output(self):
        if len(self.s_list):
            self.result_queue.put("[*] status = 200 dir:")
            print("[*] status = 200 dir:")
            for url in self.s_list:
                self.result_queue.put(url)
                print(url)
def scan_webdir(url,result_queue):
    if not url.startswith("http://"):
        url= "http://"+url
    t=webdir(url,result_queue)
    t.work()
    t.output()
