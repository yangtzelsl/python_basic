from lxml import etree

# xpath解析
# （1）本地文件                                                etree.parse
# （2）服务器响应的数据  response.read().decode('utf-8') *****   etree.HTML()

'''
xpath基本语法：
    1.路径查询
    //：查找所有子孙节点，不考虑层级关系
    / ：找直接子节点
    2.谓词查询
    //div[@id]
    //div[@id="maincontent"]
    3.属性查询
    //@class
    4.模糊查询
    //div[contains(@id, "he")]
    //div[starts‐with(@id, "he")]
    5.内容查询
    //div/h1/text()
    6.逻辑运算
    //div[@id="head" and @class="s_down"]
    //title | //price

'''

# xpath解析本地文件
tree = etree.parse('070_解析_xpath的基本使用.html')
print(tree)

#tree.xpath('xpath路径')

# 查找ul下面的li
li_list = tree.xpath('//body/ul/li')
print(li_list)

# 查找所有有id的属性的li标签
# text()获取标签中的内容
li_list = tree.xpath('//ul/li[@id]/text()')
print(li_list)

# 找到id为l1的li标签  注意引号的问题
li_list = tree.xpath('//ul/li[@id="l1"]/text()')
print(li_list)

# 查找到id为l1的li标签的class的属性值
li = tree.xpath('//ul/li[@id="l1"]/@class')
print(li)

# 查询id中包含l的li标签
li_list = tree.xpath('//ul/li[contains(@id,"l")]/text()')
print(li_list)

# 查询id的值以l开头的li标签
li_list = tree.xpath('//ul/li[starts-with(@id,"c")]/text()')
print(li_list)

#查询id为l1和class为c1的
li_list = tree.xpath('//ul/li[@id="l1" and @class="c1"]/text()')
print(li_list)

li_list = tree.xpath('//ul/li[@id="l1"]/text() | //ul/li[@id="l2"]/text()')

# 判断列表的长度
print(li_list)
print(len(li_list))

