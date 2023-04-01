import os
import sys
# 获取当前文件的绝对路径
absolute_path = os.path.abspath(__file__)


print(absolute_path)
print(sys.path[0])
filename = os.path.abspath(os.path.dirname(__file__))+r'\..\data\data.json'
print(filename)