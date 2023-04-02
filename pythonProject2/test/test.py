import requests
import sys
import threading
import time
url = "https://www.baidu.com"
t = requests.get(url).text
s = len(t)
print(s)
print(t)
