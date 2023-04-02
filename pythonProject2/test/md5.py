import hashlib

addStr = 'TSw8BK8m'
knownMd5 = 'd3b6da'

dict = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def md5(text):
    return hashlib.md5(str(text).encode('utf-8')).hexdigest()

for i in dict:
  for j in dict:
      for k in dict:
          for l in dict:
            x = i + k + j + l
            codeMd5 = md5(x)
            if codeMd5[:6] == '14742c':
                print(x)