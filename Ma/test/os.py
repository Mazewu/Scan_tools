import os
import sys
# 获取当前文件的绝对路径
absolute_path = os.path.abspath(__file__)


filename = os.path.join(sys.path[0], "data", "dir.txt")
print(filename)
print(os.getcwd())