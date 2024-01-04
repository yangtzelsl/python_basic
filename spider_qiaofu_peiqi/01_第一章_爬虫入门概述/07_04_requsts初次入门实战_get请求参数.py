import requests

url = "https://movie.douban.com/j/chart/top_list"

hehe = {
    "type": "13",
    "interval_id": "100:90",
    "action": "",
    "start": "0",
    "limit": "20"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}

resp = requests.get(url, params=hehe, headers=headers)  # 处理一个小小的反爬
# print(resp.text)
print(resp.json())
print(resp.request.url)