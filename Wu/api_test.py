import socket
import sys
import requests
import csv

def api_check(Url):
    api_list=[]
    for api_data in open('api.txt', encoding='utf-8'):
        api_data = api_data.replace('\n', '')
        url = 'https://'+ Url + api_data
        api_list.append(url)
        r=requests.get(url)
        if r.status_code==200:
            status='该网址存在'
            print(url+' '+status)
            with open('api9.csv', 'w', encoding='gbk') as f:
                for line in api_list:
                    f.write(line.strip() + '\n')
        else:
            status = '该网址不存在'
        # print(url+' '+str(r.status_code))

    # with open('api7.csv','w',encoding='gbk') as f:
    #     for line in api_list:
    #         f.write(line.strip()+'\n')








url=input()
api_check(url)
# if __name__ == '__main__':
#     check=sys.argv[1]
#     Url=sys.argv[2]
#     if check =='api':
#         api_check(Url)