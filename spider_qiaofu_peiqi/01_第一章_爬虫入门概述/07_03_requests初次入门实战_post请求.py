import requests

url = "https://fanyi.baidu.com/sug"

hehe = {
    "kw": input("请输入一个单词")
}

resp = requests.post(url, data=hehe)

print(resp.text)  # 拿到的是文本字符串
print(resp.json())  # 此时拿到的直接是json数据
