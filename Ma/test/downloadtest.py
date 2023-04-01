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
        _str = r.content.decode('utf-8')
        print(_str)
        return _str

    def post(self, url, data):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
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
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                'Content-Type': 'text/html; charset=utf-8'
            }
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code != 200:
                return None
            _str["html"] = r.content.decode('utf-8')
        except Exception as e:
            return None
        htmls.append(_str)

if __name__=="__main__":
    t= Download()
    html=t.get("https://www.zhihu.com/question/553741419/answer/2676465629")
