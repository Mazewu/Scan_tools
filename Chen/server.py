import urllib.request

print()
print("====================>请输入网址：")
custom_url = input()
file = urllib.request.urlopen(custom_url)
print(f"网页 server 为：{file.info()['Server']}")