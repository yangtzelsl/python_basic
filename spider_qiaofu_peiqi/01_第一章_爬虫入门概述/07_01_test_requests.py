import requests

# 爬取百度的页面源代码
url = "http://www.baidu.com"
resp = requests.get(url)
resp.encoding = "utf-8"
print(resp.text)  # 拿到页面源代码

