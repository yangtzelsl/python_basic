
import time

import schedule

from probe import UrlProbe, SqlProbe
from robot import DingTalkRobot, WechatRobot

"""
项目说明：用python写一个预警机器人（支持微信和钉钉）
参考文献：
    http://www.xetlab.com/2019/03/13/%E7%94%A8python%E5%86%99%E4%B8%80%E4%B8%AA%E7%AE%80%E5%8D%95%E9%A2%84%E8%AD%A6%E6%9C%BA%E5%99%A8%E4%BA%BA%EF%BC%88%E6%94%AF%E6%8C%81%E5%BE%AE%E4%BF%A1%E5%92%8C%E9%92%89%E9%92%89%EF%BC%89/?utm_source=tuicool&utm_medium=referral
    https://github.com/huangyemin/robotprobe
"""

webhook = 'https://oapi.dingtalk.com/robot/send?access_token=xxxxx'
bot = DingTalkRobot(webhook)

# bot = WechatRobot([u"研发部", u"运维部", u"someone you hate"])
# bot.run_embed()

# 每20秒检测百度网站是否正常，如果不正常超3次，则预警
baidu_probe = UrlProbe("百度", 20, 3)
baidu_probe.url = "https://www.baidux.com"

# 每30秒检测在线用户数是否太高，如果不正常达到1次，则预警
online_user_probe = SqlProbe("在线用户数", 30, 1)
online_user_probe.sql = "select count(1) from online_user"
online_user_probe.biz_threshold = 50000
online_user_probe.biz_tpl = "当前在线用户数%s，达到阈值%s"

probes = [baidu_probe, online_user_probe]


def notify_latest_state():
    for p in probes:
        if p.warning:
            bot.send_text(p.name + "异常：" + p.warning_msg)
        else:
            bot.send_text(p.name + "正常")


def send_warning(msg):
    bot.send_text(msg)


def trigger_probe(p):
    p.test()
    if p.warning:
        send_warning(p.consume_warning())


schedule.every().day.at("09:00").do(notify_latest_state)

for probe in probes:
    schedule.every(probe.interval).seconds.do(trigger_probe, probe)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
        print("I am alive！")