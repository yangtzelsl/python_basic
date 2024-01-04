import re

# result = re.findall("a", "我是一个abcdeafg")
# print(result)

# result = re.findall(r"\d+", "我今年18岁, 我有200000000块")
# print(result)


# # 这个是重点. 多多练习
# result = re.finditer(r"\d+", "我今年18岁, 我有200000000块")
# for item in result:  # 从迭代器中拿到内容
#     print(item.group())  # 从匹配到的结果中拿到数据


# search只会匹配到第一次匹配的内容
# result = re.search(r"\d+", "我叫周杰伦, 今年32岁, 我的班级是5年4班")
# print(result.group())


# # match, 在匹配的时候. 是从字符串的开头进行匹配的, 类似在正则前面加上了^
# result = re.match(r"\d+", "我叫周杰伦, 今年32岁, 我的班级是5年4班")
# print(result)


# # 预加载, 提前把正则对象加载完毕
# obj = re.compile(r"\d+")
# # 直接把加载好的正则进行使用
# result = obj.findall("我叫周杰伦, 今年32岁, 我的班级是5年4班")
# print(result)


# 想要提取数据必须用小括号括起来. 可以单独起名字
# (?P<名字>正则)
# 提取数据的时候. 需要group("名字")
s = """
<div class='西游记'><span id='10010'>中国联通</span></div>
<div class='西游记'><span id='10086'>中国移动</span></div>
"""
obj = re.compile(r"<span id='(?P<hahahahah>\d+)'>(?P<asdfasfasf>.*?)</span>")

result = obj.finditer(s)
for item in result:
    id = item.group("hahahahah")
    print(id)
    name = item.group("asdfasfasf")
    print(name)


