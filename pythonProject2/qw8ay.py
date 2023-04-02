# -*- coding:utf-8 -*-


import sys
from lib.core.qSpider import SpiderMain
from lib.core import webcms
from importlib import reload
from lib.core import common
from lib.core import PortScan
from lib.core import webdir
from lib.core import outputer

reload(sys)

def main():
    # root = "http://61.178.77.7"
    root = "http://www.baidu.com"
    threadNum: int = 10
    ip = common.gethostbyname(root)
    output = outputer.outputer()
    domain = common.qurlparse(root)
    # print("ip:", ip)
    # print("Start Port Scan:")
    # pp = PortScan.PortScan(ip)
    # pp.work()
    # spider
    w8 = SpiderMain(root, threadNum)
    w8.craw()
    # webdir
    # qdir = webdir.webdir(root, threadNum)
    # qdir.work()
    # qdir.output()
    # output.build_html(domain)
     #webcms
    # ww = webcms.webcms(root, threadNum)
    # ww.run()
    # output.build_html(domain)


if __name__ == '__main__':
    main()
