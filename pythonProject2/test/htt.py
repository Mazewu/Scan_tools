import requests



for i in range(1000):
    url = "http://59.110.159.206:7010/?id=%s" % i
    try:
        t = requests.get(url)
        code = t.status_code
        if code == 200:
            print(t.text)
    except:
        pass



