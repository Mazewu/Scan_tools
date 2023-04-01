import queue
import hashlib
import json
import os
from urllib.parse import urlparse

#注意：如果单独运行本文件，则将下面换为import Download
import lib.Download as Download

class webcms(object):
    workQueue = queue.Queue()
    URL = ""
    NotFound = True
    Downloader = Download.Download()
    result = ""

    def __init__(self, url,result_queue):
        self.result_queue=result_queue
        if not url.startswith("http://"):
            url="http://"+url
        self.qURL = url
        self.URL = urlparse(url)
        filename = os.path.abspath(os.path.dirname(__file__))+r'\..\data\data.json'
        with open(filename, encoding='UTF-8') as fp:
            webdata = json.load(fp)
            for i in webdata:
                self.workQueue.put(i)
        fp.close()

    def getmd5(self, body):
        m2 = hashlib.md5()
        m2.update(body.encode('utf-8'))
        return m2.hexdigest()

    def th_whatweb(self):
        if self.workQueue.empty():
            self.NotFound = False
            return False

        if self.NotFound is False:
            return False
        cms = self.workQueue.get()
        _url = self.URL.scheme + "://" + self.URL.netloc + cms["url"]
        html = self.Downloader.get(_url)
        self.result_queue.put("[whatweb log]:checking %s" % _url)
        print("[whatweb log]:checking %s" % _url)
        if html is None:
            return False
        if cms["re"]:
            if html.find(cms["re"]) != -1:
                self.result = cms["name"]
                self.NotFound = False
                return True
        else:
            md5 = self.getmd5(html)
            if md5 == cms["md5"]:
                self.result = cms["name"]
                self.NotFound = False
                return True

    def run(self):
        while self.NotFound:
            self.th_whatweb()
        if self.result:
            self.result_queue.put("[webcms]:%s cms is %s" % (self.qURL, self.result))
            print("[webcms]:%s cms is %s" % (self.qURL, self.result))
        else:
            self.result_queue.put("[webcms]:%s cms NOTFound!" % self.qURL)
#对图形化的接口函数
def cmscheck(url,result_queue):
    t=webcms(url=url,result_queue=result_queue)
    t.run()


#test
if __name__=="__main__":
    result_queue=queue.Queue()
    t=webcms(url="http://www.sina.com",result_queue=result_queue)
    t.run()
#"http://61.178.77.7"
