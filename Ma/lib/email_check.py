import re
import lib.Download as Download
import queue
Downloader = Download.Download()
def email_check(url,result_queue):
    result_queue.put("开始查找网页邮箱...")
    if not url.startswith("http://"):
        url = "http://"+url
    html=Downloader.get(url)
    pattern = re.compile(r'([\w-]+@[\w-]+\.[\w-]+)+')
    email_list = re.findall(pattern, html)
    if email_list:
        for email in email_list:
            result_queue.put(("email:"+ email))
        result_queue.put("查找完毕！")
        return True
    result_queue.put("没有查询到邮箱！")
    return False


