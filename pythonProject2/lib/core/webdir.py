import os
import sys
import queue
import requests
import threading
from urllib.parse import urlparse
from lib.core import outputer
output = outputer.outputer()

class webdir:
    def __init__(self, root, threadNum):
        self.root = urlparse(root)
        self.threadNum = threadNum
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
            'Referer': 'http://www.shiyanlou.com',
            'Cookie': 'whoami=who',
        }
        self.task = queue.Queue()
        self.s_list = []
        filename = os.path.join(sys.path[0], "data", "dir.txt")
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
                output.add_list("Web_Path", url)
            print("Testing: %s status:%s"%(url, s_code))


    def work(self):
        threads = []
        for i in range(self.threadNum):
            t = threading.Thread(target=self.test_url())
            threads.append(t)
            t.start()
        for i in threads:
            t.join()
        print('[*] The DirScan is complete!')

    def output(self):
        if len(self.s_list):
            print("[*] status = 200 dir:")
            for url in self.s_list:
                print(url)

