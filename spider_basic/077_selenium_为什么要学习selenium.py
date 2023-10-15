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
import urllib.request

url = 'https://www.jd.com/'

response = urllib.request.urlopen(url)

content = response.read().decode('utf-8')

print(content)