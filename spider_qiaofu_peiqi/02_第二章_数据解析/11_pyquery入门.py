from pyquery import PyQuery

# html = """
#     <ul>
#        <li class="aaa"><a href="http://www.google.com">谷歌</a></li>
#        <li class="aaa"><a href="http://www.baidu.com">百度</a></li>
#        <li class="bbb" id="qq"><a href="http://www.qq.com">腾讯</a></li>
#        <li class="bbb"><a href="http://www.yuanlai.com">猿来</a></li>
#    </ul>
# """
#
# # 加载html内容
# p = PyQuery(html)

# print(p)
# print(type(p))
# pyquery对象直接(css选择器)

# a = p("a")
# print(a)
# print(type(a))  # 依然是pyquery对象

# # 链式操作
# a = p("li")("a")
# print(a)

# a = p("li a")
# print(a)

# a = p(".aaa a")  # class="aaa"
# print(a)

# a = p("#qq a")  # id="qq"
# print(a)

# href = p("#qq a").attr("href")  # 拿属性
# text = p("#qq a").text()  # 拿文本
# print(text)

# 坑, 如果多个标签同时拿属性. 只能默认拿到第一个
# href = p("li a").attr("href")
# print(href)

# # 多个标签拿属性
# it = p("li a").items()
# for item in it:  # 从迭代器中拿到每一个标签
#     href = item.attr("href")  # 拿到href属性\
#     text = item.text()
#     print(text, href)


# 快速总结:
# 1. pyquery(选择器)
# 2. items()  当选择器选择的内容很多的时候. 需要一个一个处理的时候
# 3. attr(属性名)  获取属性信息
# 4. text() 获取文本


# div = """
#     <div><span>我爱你</span></div>
# """
# p = PyQuery(div)
# html = p("div").html()  # 全都要
# text = p("div").text()  # 只要文本, 所有的HTML标签被过滤掉
# print(html)
# print(text)

html = """
<HTML>
    <div class="aaa">哒哒哒</div>
    <div class="bbb">嘟嘟嘟</div>
</HTML>
"""

p = PyQuery(html)

# 在xxxx标签后面添加xxxxx新标签
# p("div.aaa").after("""<div class="ccc">吼吼吼</div>""")
# p("div.aaa").append("""<span>我爱你</span>""")

# p("div.bbb").attr("class", "aaa")  # 修改属性
# p("div.bbb").attr("id", "12306")  # 新增属性, 前提是该标签没有这个属性
# p("div.bbb").remove_attr("id")  # 删除属性
# p("div.bbb").remove()  # 删除标签
# print(p)

# dic = {}
# dic['jay'] = "周杰伦"
# print(dic)
# dic['jay'] = "呵呵哒"
# print(dic)
