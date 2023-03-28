import socket
import sys


def zym_check(url):
    urls=url.replace('www','')
    for zym_data in open('sub11.txt',encoding='utf-8'):
        zym_data=zym_data.replace('\n','')
        url = zym_data +urls
        try:
            ip=socket.gethostbyname(url)
            print(url+'->'+ip)
        except Exception as e:
            pass


if __name__ == '__main__':
    check=sys.argv[1]
    urls=sys.argv[2]
    if check =='zym':
        zym_check(urls)