import socket
import os

#当前文件所在文件夹的绝对路径
dir_path = os.path.abspath(os.path.dirname(__file__))

# 扫描子域名模块
def zym_check(url, result_queue):
    result_queue.put('开始扫描网站子域名...')
    urls = url.replace('www', '')
    for zym_data in open(dir_path+r"\..\data\sub11.txt", encoding='utf-8'):
        zym_data = zym_data.replace('\n', '')
        url = zym_data + urls
        try:
            ip = socket.gethostbyname(url)
            result_queue.put(url + ' -> ' + ip)
        except Exception as e:
            pass
    result_queue.put('[zym_check] The scan is complete!')