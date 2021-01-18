import requests


def get_method():
    # 1. 最基本的GET请求可以直接用get方法
    response1 = requests.get("http://www.baidu.com/")
    # 也可以这么写
    response2 = requests.request("get", "http://www.baidu.com/")

    kw = {'wd': '长城'}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

    # params 接收一个字典或者字符串的查询参数，字典类型自动转换为url编码，不需要urlencode()
    response = requests.get("http://www.baidu.com/s?", params=kw, headers=headers)
    # 查看响应内容，response.text 返回的是Unicode格式的数据
    print(response.text)
    # 查看响应内容，response.content返回的字节流数据
    print(response.content)
    # 查看完整url地址
    print(response.url)
    # 查看响应头部字符编码
    print(response.encoding)
    # 查看响应码
    print(response.status_code)


def post_method():
    # 1. 最基本的GET请求可以直接用post方法
    data = {}
    response = requests.post("http://www.baidu.com/", data=data)

    # 2.传入data数据
    formdata = {
        "type": "AUTO",
        "i": "i love python",
        "doctype": "json",
        "xmlVersion": "1.8",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_ENTER",
        "typoResult": "true"
    }

    url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}

    response = requests.post(url, data=formdata, headers=headers)
    print(response.text)

    # 如果是json文件可以直接显示
    print(response.json())
