#!/usr/bin/env python

# coding: utf8

import json
import sys
import time

import urllib2

reload(sys)

sys.setdefaultencoding('utf-8')

myfile = sys.stdin

data = json.load(myfile)

for i in range(0, len(data)):

    alert = data[i]["body"]["alert"]["attributes"]

    alertSummary = alert["ALERT_SUMMARY"]

    for summary in alertSummary:
        print("ALERT_SUMMARY: ",)
        print(summary)
    healthResult = alert["HEALTH_TEST_RESULTS"]

    for result in healthResult:
        print("content: ",)
        print(result["content"])
        print("testName: ",)
        print(result["testName"])

    print("")

    # 企业号ID
    wxid = "wwXXX"
    # 应用ID
    depid = "100001111"
    # 认证密码
    secret = "U37SXXXXXXXXXXX"
    msg = result["content"]
    # 获取当前的时间
    date_time = time.strftime("%Y-%m-%d %X")
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + wxid + "&corpsecret=" + secret

request = urllib2.Request(url)

response = urllib2.urlopen(request)

recv_info = response.read()

recv_info = eval(recv_info)

wx_token = recv_info['access_token']

msg_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + wx_token

send_msg = {

    "touser": "@all",
    "msgtype": "text",
    "agentid": depid,
    "text": {"content": msg},
    "safe": 0
}

send_msg_json = json.dumps(send_msg)

request_post = urllib2.urlopen(msg_url, send_msg_json)

recv_msg = request_post.read()
