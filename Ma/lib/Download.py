import requests
from bs4 import BeautifulSoup

class Download(object):
    def get(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return None
        _str = r.text
        return _str

    def post(self, url, data):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        r = requests.post(url, data, headers=headers)
        _str = r.text
        print(_str)
        return _str

    def download(self, url, htmls):
        if url is None:
            return None
        _str = {}
        _str["url"] = url
        try:
            headers = {
                'Content-Type': 'text/html; charset=utf-8'
            }
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code != 200:
                return None
            _str["html"] = r.text
        except Exception as e:
            return None
        htmls.append(_str)

if __name__=="__main__":
    t= Download()
    html=t.get("https://movie.douban.com/top250?start=0&filter=")
    print(html)

