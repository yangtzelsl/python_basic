# 登录 -> 得到cookie
# 带着cookie 去请求到书架url -> 书架上的内容

# 必须得把上面的两个操作连起来
# 我们可以使用session进行请求 -> session你可以认为是一连串的请求. 在这个过程中的cookie不会丢失
import requests

# # 会话
# session = requests.session()
# data = {
#     "loginName": "18614075987",
#     "password": "q6035945"
# }
#
# # 1. 登录
# url = "https://passport.17k.com/ck/user/login"
# session.post(url, data=data)
# # print(resp.text)
# # print(resp.cookies)  # 看cookie
#
# # 2. 拿书架上的数据
# # 刚才的那个session中是有cookie的
# resp = session.get('https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919')
#
# print(resp.json())

resp = requests.get("https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919", headers={
    "Cookie":"GUID=423006e8-aac0-4537-b638-598ff7e9e9d7; sajssdk_2015_cross_new_user=1; Hm_lvt_9793f42b498361373512340937deb2a0=1704471543; _openId=ow-yN5sIc4cvT9cDnDnh4F4YktxM; accessToken=nickname%3D%25E4%25B9%25A6%25E5%258F%258B19vtO6346%26avatarUrl%3Dhttps%253A%252F%252Fcdn.static.17k.com%252Fuser%252Favatar%252F15%252F55%252F65%252F102826555.jpg-88x88%253Fv%253D1704471575225%26id%3D102826555%26e%3D1720023578%26s%3D7401e8105826c279; c_channel=0; c_csc=web; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22102826555%22%2C%22%24device_id%22%3A%2218cda6bbd95108a-07c1dc8e3b90f9-26031051-2073600-18cda6bbd961808%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%A4%BE%E4%BA%A4%E7%BD%91%E7%AB%99%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fopen.weixin.qq.com%2F%22%2C%22%24latest_referrer_host%22%3A%22open.weixin.qq.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%2C%22first_id%22%3A%22423006e8-aac0-4537-b638-598ff7e9e9d7%22%7D; ssxmod_itna=Qqfx2D9D0DgDRD020DzxA2i=GkWFMF+q2D4mKq+KDsKeWDSxGKidDqxBeP6Pm4pqPwWDOu343KG37d+38O0x+aQQllfK3DU4i8DCkGq=+xeetD5xGoDPxDeDAiKiTDY4Dd6xYPG0DiKGRDB=XnqDjYDoDzxrP8qGE/qDgBSNDIqtPDDNPBWxe9DDwDPGW8wtU+lNDKqDSKGtqQA=DjLbD/+DkkeDBU=HP0wUHw1natd0DxBQD7MX9DYoXWPDHGktSKPYdF2xdABvYAGGFK0DY70+mi0Mx7iYNh0hWAACYt03YKBvQ/EsDGR3O0kKiDD=; ssxmod_itna2=Qqfx2D9D0DgDRD020DzxA2i=GkWFMF+q2D4mKq4ikfKKFqDlhnxj4RDT6P4qWQGFQWTr=qRe8jKxet4tjAmGtY8e+pvahldO2bTLIYKWwkDHmTidh=djYif+P+AKiYpstA/Zn0oWNxwiBEVIqNhnqtnKn6SC7A/3nhB8wtBGj6e17=gK4AxiuQoco=1e+nx1B=5nd=axmUn4erx5MUKp1=h9DXH9L9kgnQ=2kc8IC0yFMvyCEF12DNd5Du7U=+8gcNlmmR7ncD/bP0VbTHb=M=Wwrg+xnZmeM6FTV1O6vrR45of+vL/heHbemYiinu+4+9fK6GuhnrAWq/Rbl8w/K58/RsiTxsP45G42uDK7YcFCKWo7TQK01GYcjvO9W7KWGGAuGYXiB8GAKgIexYzSvylmo5udOvwSpekKllFHQ4At8qg+/Cbb/W6I5l3HPLuFxqiBewSv0/fyQIljyWsvq7Dqb71AyTzqXSq5DWLFxDKu43Y4wEYnG3YGXMAXV0Ox/Ke9PI2DPoPSDkpi3tqR5wNt7qD7=DYI4eD=; Hm_lpvt_9793f42b498361373512340937deb2a0=1704471683"
})
print(resp.text)