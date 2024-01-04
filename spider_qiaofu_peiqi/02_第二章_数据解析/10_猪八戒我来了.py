"""
1. 拿到页面源代码
2. 从页面源代码中提取你需要的数据. 价格, 名称, 公司名称

"""
import requests
from lxml import etree

url = "https://beijing.zbj.com/search/f/?type=new&kw=saas"
resp = requests.get(url)
resp.encoding = "utf-8"
# print(resp.text)

# 提取数据
et = etree.HTML(resp.text)
divs = et.xpath("//div[@class='new-service-wrap']/div")
for div in divs:
    # 此时的div就是一条数据. 对应一个商品信息
    # 商品价格
    price = div.xpath("./div/div/a/div[2]/div[1]/span[1]/text()")
    if not price:  # 过滤掉无用的数据
        continue
    price = price[0]
    company = div.xpath("./div/div/a[2]/div[1]/p/text()")[0]
    # name = div.xpath("./div/div/a[1]/div[2]/div[2]/p//text()")  # //表示提取p的所有文本, 包括子子孙孙所有内容
    # name = "".join(name)
    print(company)
    break


# r = "_".join(["张无忌", "麻花藤", "码云"])
# print(r)
