"""
1, 提取页面源代码
2, 解析页面源代码. 提取数据
"""
import requests
from pyquery import PyQuery


def get_page_source(url):
    resp = requests.get(url)
    resp.encoding = "gbk"
    return resp.text


def parse_page_source(html):
    doc = PyQuery(html)
    mt_list = doc(".mt-10").items()  # class="mt-10"
    for mt in mt_list:  # 拿到每一个mt

        # 判断是否有汽车经销商
        if not mt("div > dl:nth-child(3) > dt:contains(购车经销商)"):
            # 向 地点 后添加购车经销商进去
            mt("div > dl:nth-child(2)").after(PyQuery("""<dl class="choose-dl">
                        <dt>购车经销商</dt>
                        <dd>
                            <a href="###" class="js-dearname" data-val='125965,47759' data-evalid="3629818" target="_blank">
                                &nbsp
                            </a>
                        </dd>
                    </dl>"""))

        # 提取购买的车型
        # 想要在已经提取的内容中获取第一个怎么办?  eq(0)
        # nth-child(1) 在css进行选择的时候.选取第1个位置的内容
        chexing = mt("div > dl:nth-child(1) > dd").eq(0).text().replace("\n", "").replace(" ", "")
        didian = mt("div > dl:nth-child(2) > dd").text()
        shijian = mt("div > dl:nth-child(4) > dd").text()
        jiage = mt("div > dl:nth-child(5) > dd").text().replace(" 万元", "")
        youhao = mt("div > dl:nth-child(6) > dd > p:nth-child(1)").text().replace(" 升/百公里", "")
        gonglishu = mt("div > dl:nth-child(6) > dd > p:nth-child(2)").text().replace(" 公里", "")
        other = mt("div > div > dl > dd").text().split()
        print(other)
        # 存储到文件中.......


def main():
    url = "https://k.autohome.com.cn/146/"
    # 1, 提取页面源代码
    html = get_page_source(url)
    # 2, 解析页面源代码.提取数据
    parse_page_source(html)


if __name__ == '__main__':
    main()
