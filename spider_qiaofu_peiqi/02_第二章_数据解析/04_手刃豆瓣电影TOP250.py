# 思路,
# 1. 拿到页面源代码
# 2. 编写正则, 提取页面数据
# 3. 保存数据
import requests
import re

f = open("top250.csv", mode="w", encoding='utf-8')


url = "https://movie.douban.com/top250?start=200&filter="

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}

resp = requests.get(url, headers=headers)
# resp.encoding = 'utf-8'  # 解决乱码问题.
pageSource = resp.text


# 编写正则表达式
# re.S 可以让正则中的.匹配换行符
obj = re.compile(r'<div class="item">.*?<span class="title">(?P<name>.*?)</sp'
                 r'an>.*?<p class="">.*?导演: (?P<dao>.*?)&nbsp;.*?<br>'
                 r'(?P<year>.*?)&nbsp;.*?<span class="rating_num" property="v:average">'
                 r'(?P<score>.*?)</span>.*?<span>(?P<num>.*?)人评价</span>', re.S)

# 进行正则匹配
result = obj.finditer(pageSource)
for item in result:
    name = item.group("name")
    dao = item.group("dao")
    year = item.group("year").strip()  # 去掉字符串左右两端的空白
    score = item.group("score")
    num = item.group("num")
    f.write(f"{name},{dao},{year},{score},{num}\n")  # 如果觉着low. 可以更换成csv模块. 进行数据写入

f.close()
resp.close()
print("豆瓣TOP250提取完毕.")

# 如何翻页提取?
# (页数 - 1)*25  => start
