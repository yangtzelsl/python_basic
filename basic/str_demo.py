# 1.删除指定字符
# strip():删除字符串两边的指定字符，括号的写入指定字符，默认为空格
# lstrip():删除字符串左边的指定字符，括号的写入指定字符，默认空格
# rstrip():删除字符串右边的指定字符，括号的写入指定字符，默认空格
a = '    hello    '
b = a.strip()
print(b)
print("*" * 20, '\n')

# 2.复制字符串
a = 'hello world'
b = a
print(a, b)
print("*" * 20, '\n')

# 3.连接字符串
# +
# join
a = 'hello'
b = 'world'
print(a + b)
print(a.join(b))
print("*" * 20, '\n')

# 4.查找字符串
# str.index 和str.find 功能相同，区别在于find()查找失败会返回-1，不会影响程序运行。
# 一般用find != -1或者find > -1来作为判断条件
# str.index:检测字符串中是否包含子字符串str，可指定范围
# str.find:检测字符串中是否包含子字符串str，可指定范围
a = 'hello world'
print(a.index('l'))
# print(a.index('x')) # 没找到会报错 ValueError: substring not found

print(a.find('x'))
print(a.find('x'))
print("*" * 20, '\n')

# 5.比较字符串
# str.cmp：比较两个对象，并根据结果返回一个整数。X< Y,返回值是负数 ，X>Y 返回的值为正数。
# python3已经没有该方法，官方文档是这么写的
# 如果需要cmp()函数，你可以用表达式(a > b) - (a < b)代替cmp(a,b)
a = 100
b = 80
# print(cmp(a,b)) # 在python3中这样写语法不通过
print((a > b))  # True
print((a < b))  # False
print("*" * 20, '\n')

# 6.是否包含指定字符串
# in | not in
a = 'hello world'
print('hello' in a)
print('hello' not in a)
print("*" * 20, '\n')

# 7.字符串长度
# len()
a = 'hello world'
print(len(a))
print("*" * 20, '\n')

# 8.字母大小写转换
# lower() 全部转小写
# upper() 全部转大写
# swapcase() 大小写互换
# capitalize() 首字母大写
a = 'Hello World'
print(a.lower())
print(a.upper())
print(a.swapcase())
print(a.capitalize())
print("*" * 20, '\n')

# 9.将字符串放入中心位置,可指定长度以及位置两边字符
# str.center()
a = 'hello world'
print(a.center(40, '*'))
print("*" * 20, '\n')

# 10.字符串计数
a = 'hello world'
print(a.count('l'))
# print(a.count()) # 不能啥都不加
print("*" * 20, '\n')

# 11.字符串的测试、判断函数，这一类函数在string模块中没有，这些函数返回的都是bool值
# S.startswith(prefix[,start[,end]])   #是否以prefix开头
# S.endswith(suffix[,start[,end]])     #以suffix结尾
# S.isalnum()                          #是否全是字母和数字，并至少有一个字符
# S.isalpha()                          #是否全是字母，并至少有一个字符
# S.isdigit()                          #是否全是数字，并至少有一个字符
# S.isspace()                          #是否全是空白字符，并至少有一个字符
# S.islower()                          #S中的字母是否全是小写
# S.isupper()                          #S中的字母是否便是大写
# S.istitle()                          #S是否是首字母大写的

# 12.字符串切片
str = '0123456789'
print(str[0:3])  # 截取第一位到第三位的字符
print(str[:])  # 截取字符串的全部字符
print(str[6:])  # 截取第七个字符到结尾
print(str[:-3])  # 截取从头开始到倒数第三个字符之前
print(str[2])  # 截取第三个字符
print(str[-1])  # 截取倒数第一个字符
print(str[::-1])  # 创造一个与原字符串顺序相反的字符串
print(str[-3:-1])  # 截取倒数第三位与倒数第一位之前的字符
print(str[-3:])  # 截取倒数第三位到结尾
print(str[:-5:-3])  # 逆序截取，截取倒数第五位数与倒数第三位数之间

# 13.分割，前中后三部分
s = "alex SB alex"
ret = s.partition('SB')
print(ret)  # 输出元组  ('alex ', 'SB', ' alex')

# 14.替换
s = "alex SB alex"
ret = s.replace("al", "BB")
print(ret)  # 输出结果    BBex SB BBex

# 15.按输入字符切割
s = "alexalec"
ret = s.split("e")
print(ret)  # 输出结果    ['al', 'xal', 'c']

# 16.根据换行执行分割
s = "alex\nalec"
ret = s.splitlines()
print(ret)  # 输出结果     ['alex', 'alec']

# 17.变成标题
s = "alExAlec"
ret = s.title()
print(ret)  # 输出Alexalec

# 18.返回指定长度的字符串，原字符串右对齐，前面填充0
s = "alEx Alec"
ret = s.zfill(11)
print(ret)  # 输出结果    00alEx Alec

a = 10
b = 20
print("数据分别为：a={}, b={}".format(a,b))
