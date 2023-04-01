import urllib.request
# 扫描网站服务器模块
def server_check(url, result_queque):
    result_queque.put(f"开始识别网站server...")
    if not url.startswith("http"):
        url = "http://" + url
    file = urllib.request.urlopen(url)
    result_queque.put(f"网站server 为：{file.info()['Server']}")
    result_queque.put(f"网站server识别完毕！")