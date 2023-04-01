import requests
import os


#当前文件所在文件夹的绝对路径
dir_path = os.path.abspath(os.path.dirname(__file__))
def api_check(url, result_queue):
    result_queue.put('开始扫描网站api模块...')
    api_list = []
    Url=url
    for api_data in open(dir_path+r"\..\data\api.txt", encoding='utf-8'):
        api_data = api_data.replace('\n', '')
        url = 'https://' + Url+ api_data
        api_list.append(url)
        r = requests.get(url)
        if r.status_code == 200:
            status = '该网址存在'
            result_queue.put(url + ' ' + status)
            with open(dir_path+r'\..\data\api9.csv', 'w', encoding='gbk') as f:
                for line in api_list:
                    f.write(line.strip() + '\n')
        else:
            status = '该网址不存在'
    result_queue.put('[api_check] The scan is complete!')