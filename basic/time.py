#!/usr/bin/python3

import time

# 格式化成2016-03-20 11:45:39形式
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
# 类型是str
print(type(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
# id每次是不同的
print(id(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

print(time.strftime("%Y-%m-%d", time.localtime()))
print(time.strftime("%H:%M:%S", time.localtime()))

# 格式化成Sat Mar 28 22:24:24 2016形式
print(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))

# 将格式字符串转换为时间戳
a = "Sat Mar 28 22:24:24 2016"
print(time.mktime(time.strptime(a, "%a %b %d %H:%M:%S %Y")))

print(time.time())
# 类型是float
print(type(time.time()))
