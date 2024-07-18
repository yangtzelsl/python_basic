[TOC]

# 学习视频

尚硅谷Python爬虫教程小白零基础速通（含python基础+爬虫案例）

【Python爬虫实战】樵夫/沛齐老师教你学爬虫基础+js逆向+APP逆向（零基础小白也能学会）
https://www.bilibili.com/video/BV11W4y1f7Av/

波波老师+沛齐老师 亲授 爬虫逆向案例 (js逆向+app逆向）实战案例
https://www.bilibili.com/video/BV1c54y1M7pB/

# 爬虫基础
## urllib
## requests
```python
import requests
# 案例1. 抓取搜狗搜索内容
kw = input("请输入你要搜索的内容:")
response = requests.get(f"https://www.sogou.com/web?query={kw}") # 发送get请求
# print(response.text) # 直接拿结果(⽂本)

with open("sogou.html", mode="w", encoding="utf-8") as f:
	f.write(response.text)
```

## 正则表达式
```bash
正则的语法: 使用元字符进行排列组合用来匹配字符串 
在线测试正则表达式 https://tool.oschina.net/regex/
元字符: 具有固定含义的特殊符号 
常用元字符:

. 匹配除换⾏符以外的任意字符, 未来在python的re模块中是一个坑.
\w 匹配字目或数字或下划线
\s 匹配任意的空⽩符
\d 匹配数字
\n 匹配一个换行符
\t 匹配一个制表符
^ 匹配字符串的开始
$ 匹配字符串的结尾
\W 匹配非字母或数字或下划线
\D 匹配非数字
\S 匹配非空白符
a|b 匹配字符a或字符b
() 匹配括号内的表达式，也表示一个组
[...] 匹配字符组中的字符
[^...] 匹配除了字符组中字符的所有字符

量词: 控制前面的元字符出现的次数
* 重复零次或更多次
+ 重复一次或更多次
? 重复零次或一次
{n} 重复n次
{n,} 重复n次或更多次
{n,m} 重复n到m次

贪婪匹配和惰性匹配
.* 贪婪匹配, 尽可能多的去匹配结果
.*? 惰性匹配, 尽可能少的去匹配结果 -> 回溯
```
## re
## bs4
## xpath
- google浏览器推荐使用xpath扩展程序 xpath.crx

## pyquery
## JsonPath

## 爬虫框架scrapy
## selenium
```python
"""
1.什么是selenium？
（1）Selenium是一个用于Web应用程序测试的工具。
（2）Selenium 测试直接运行在浏览器中，就像真正的用户在操作一样。
（3）支持通过各种driver（FirfoxDriver，IternetExplorerDriver，OperaDriver，ChromeDriver）驱动
真实浏览器完成测试。
（4）selenium也是支持无界面浏览器操作的。

2.为什么使用selenium？
模拟浏览器功能，自动执行网页中的js代码，实现动态加载

3.如何安装selenium？
（1）操作谷歌浏览器驱动下载地址
http://chromedriver.storage.googleapis.com/index.html
（2）谷歌驱动和谷歌浏览器版本之间的映射表
http://blog.csdn.net/huilan_same/article/details/51896672
（3）查看谷歌浏览器版本
谷歌浏览器右上角‐‐>帮助‐‐>关于
（4）pip install selenium

4.selenium的使用步骤？
（1）导入：from selenium import webdriver
（2）创建谷歌浏览器操作对象：
path = 谷歌浏览器驱动文件路径
browser = webdriver.Chrome(path)
（3）访问网址
url = 要访问的网址
browser.get(url)

4‐1：selenium的元素定位？
元素定位：自动化要做的就是模拟鼠标和键盘来操作来操作这些元素，点击、输入等等。操作这些元素前首先
要找到它们，WebDriver提供很多定位元素的方法
方法：
1.find_element_by_id
eg:button = browser.find_element_by_id('su')
2.find_elements_by_name
eg:name = browser.find_element_by_name('wd')
3.find_elements_by_xpath
eg:xpath1 = browser.find_elements_by_xpath('//input[@id="su"]')
4.find_elements_by_tag_name
eg:names = browser.find_elements_by_tag_name('input')
5.find_elements_by_css_selector
eg:my_input = browser.find_elements_by_css_selector('#kw')[0]
6.find_elements_by_link_text
eg:browser.find_element_by_link_text("新闻")
"""
```

## cookies
## 防盗链
## 代理


# JS逆向 & Web逆向
## 环境准备

- js调试工具(发条JS调试工具1.8)
- PyExecJs(pip install PyExecJs)

```python
import execjs

# 1.实例化一个node对象
node = execjs.get()

# 2.js源文件编译
ctx = node.compile(open('./wechat.js', encoding='utf-8').read())

# 3.执行js函数
func_name = 'getPwd("{0}")'.format('123456')
pwd = ctx.eval(func_name)
print(pwd)
```

## 案例分享(波波老师)

- 微信公众平台 - md5
- steam - rsa
- 凡科网
- 完美世界
- 试客联盟
- 空中网
- 长房网
- 有道翻译
- 空气质量

## 案例分享(沛奇)

- x视频
- x头条
- x站播放量



# App逆向

## 环境准备

- 设备(真机、模拟器)逍遥、夜神、网易mumu
- 目标软件apk安装包
- 抓包软件(charles)
- 反编译工具(jadx、jeb、jda)

## 案例分享(沛奇)

- 藏航
- 油联合伙人