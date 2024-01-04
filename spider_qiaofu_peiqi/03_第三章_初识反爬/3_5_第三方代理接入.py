import requests


def get_ip():
    while 1:  # 反复提取代理IP
        # 有待完善. 如果代理ip都用完了. 怎么办????
        url = "http://dev.kdlapi.com/api/getproxy/?orderid=902718903050420&num=100&protocol=2&method=1&an_an=1&an_ha=1&quality=1&format=json&sep=1"
        resp = requests.get(url)
        ips = resp.json()
        if ips['code'] == 0:
            for ip in ips['data']['proxy_list']:  # 拿到每一个ip
                print("即将返回ip", ip)
                yield ip   # 一个一个返回代理ip
            print("所有IP已经用完, 即将更新!")  # for循环结束. 继续提取新IP
        else:
            print("获取代理IP出现异常. 重新获取!")



def spider():
    url = "https://www.dy2018.com/"
    while 1:
        try:
            proxy_ip = next(gen)  # 拿到代理ip
            proxy = {
                "http": "http://" + proxy_ip,
                "https": "https://" + proxy_ip,
            }
            print(proxy)
            proxy = {
                'http': 'http://118.117.188.32:3256',
                'https': 'https://118.117.188.32:3256'
            }
            proxy = {
                'http': 'http://182.84.145.178:3256',
                'https': 'https//182.84.145.178:3256'
            }
            resp = requests.get(url, proxies=proxy, timeout=20)
            resp.encoding = "utf-8"
            return resp.text
        except :
            print("报错了. ")


if __name__ == '__main__':
    gen = get_ip()  #  gen就是代理ip的生成器
    for i in range(10):
        print(spider())
