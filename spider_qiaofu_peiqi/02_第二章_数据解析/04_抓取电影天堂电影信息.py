"""
1. 提取到主页面中的每一个电影的背后的那个url地址
    1. 拿到 "2021必看热片" 那一块的HTML代码.
    2. 从刚才拿到的HTML代码中提取到href的值

2. 访问子页面, 提取到电影的名称以及下载地址
    1. 拿到子页面的页面源代码
    2. 数据提取
"""
import requests
import re


url = "https://www.dy2018.com/"
resp = requests.get(url)
resp.encoding = "gbk"
# print(resp.text)


# 1.提取2021必看热片部分的HTML代码
obj1 = re.compile(r"2021必看热片.*?<ul>(?P<html>.*?)</ul>", re.S)
result1 = obj1.search(resp.text)
html = result1.group("html")

# 2.提取a标签中的href的值
obj2 = re.compile(r"<li><a href='(?P<href>.*?)' title")

result2 = obj2.finditer(html)

obj3 = re.compile(r'<div id="Zoom">.*?◎片　　名(?P<movie>.*?)<br />.*?<td style="WORD-WRAP: break-word"'
                  r' bgcolor="#fdfddf"><a href="(?P<download>.*?)">', re.S)
for item in result2:
    # print(item.group("href"))
    # 拼接出子页面的url
    child_url = url.strip("/") + item.group("href")
    child_resp = requests.get(child_url)
    child_resp.encoding = 'gbk'

    result3 = obj3.search(child_resp.text)
    movie = result3.group("movie")
    download = result3.group("download")
    print(movie, download)
