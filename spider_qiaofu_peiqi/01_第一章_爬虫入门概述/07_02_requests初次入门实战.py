import requests

content = input('请输入你要检索的内容:')
url = f"https://www.sogou.com/web?query={content}"

headers = {
    # 添加一个请求头信息. UA
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}
# 处理一个小小的反爬
resp = requests.get(url, headers=headers)
print(resp.text)

print(resp.request.headers)  # 可以查看到请求头信息
