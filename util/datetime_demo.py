import datetime

"""
谨记：文件名命名时，不要和内置模块同名
"""
# 时间获取
print(datetime.datetime.now())

# 时间格式化
print((datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
print(datetime.datetime.now().strftime("%Y%m%d"))

# 时间加减
print((datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"))
print((datetime.datetime.now()+datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
print((datetime.datetime.now()+datetime.timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S"))
