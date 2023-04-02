import pandas as pd
from io import StringIO
import numpy as np

#csv_file = StringIO('D:\data\winequality-red1.csv'
data=("""0,1,2,3,4,5
1,2,1,3.5,6,8.5
2,0.83,0.9,0.85,0.8,0.75
3,1.0,1.0,0.95,0.9,0.85
4,0.89,0.95,0.9,0.85,0.8
5,0.92,1.0,0.95,0.9,0.85
6,1.6,1.8,1.6,1.4,1.2""")


csv_data = pd.read_csv(StringIO(data), low_memory=False)
x = pd.DataFrame(csv_data)
x = x.iloc[:, 1:].T

# 1、数据序列预处理
#x_mean = x.mean(axis=1)
#x_max = x.max(axis=1)
#x_min = x.min(axis=1)
#for i in range(x.index.size):
#    x.iloc[i, :] = x.iloc[i, :] / x_mean[i]
#    x.iloc[i,:] = x.iloc[i,:]/x_min[i]
#    x.iloc[i,:] = x.iloc[i,:]/x_max[i]

# 2、提取参考队列和比较队列
ck = x.iloc[0, :]
cp = x.iloc[1:, :]

# 比较队列与参考队列相减
t = pd.DataFrame()
for j in range(cp.index.size):
    temp = pd.Series(cp.iloc[j, :] - ck)
    t = t.append(temp, ignore_index=True)

# 求最大差和最小差
mmax = t.abs().max().max()
mmin = t.abs().min().min()
rho = 0.5

# 3、求关联系数
ksi = ((mmin + rho * mmax) / (abs(t) + rho * mmax))

# 4、求关联度
r = ksi.sum(axis=1) / ksi.columns.size

# 5、关联度排序

result = r.sort_values(ascending=False)
print(result)
