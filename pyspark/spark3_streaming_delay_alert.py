# -*- coding:UTF-8 -*-

import os
import re
import sys
import json
from optparse import OptionParser

import requests
from lxml import etree


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


def option_parser():
    usage = "usage: %prog [options] arg1"

    parser = OptionParser(usage=usage)

    parser.add_option("--application_name", dest="application_name", action="store", type="string", help="")
    parser.add_option("--active_batches", dest="active_batches", action="store", type="string", help="")

    return parser


def robot(key, data):
    # 企业微信机器人的 webhook
    # 开发文档 https://work.weixin.qq.com/api/doc#90000/90136/91770
    webhook = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}"
    headers = {'content-type': 'application/json'}  # 请求头
    r = requests.post(webhook, headers=headers, data=json.dumps(data))
    r.encoding = 'utf-8'
    # print(f'执行内容:{data}, 参数:{r.text}')
    # print(f'webhook 发送结果:{r.text}')
    return r.text


def bot_push(key, data):
    try:
        res = robot(key, data)
        print(f'webhook 发出完毕: {res}')
        return res
    except Exception as e:
        print(e)


def bot_push_markdown(key, msg):
    """
    发送markdown格式的消息
    """
    webhook_data = {
        "msgtype": "markdown",
        "markdown": {
            "content": "<font color=\"warning\">神策实时任务延时，请相关同事注意。</font>\n\
            >任务名称: <font color=\"comment\">" + msg["application_name"] + "</font>\n\
            >任务所在机器: <font color=\"comment\">" + msg["ip"] + "</font>\n\
            >任务链接: ["+msg["streaming_url"]+"](" + msg["streaming_url"] + ")\n\
            >积压批次数量: <font color=\"comment\">" + str(msg["active_batch"]) + "</font>\n\
            >当前批次处理的记录数: <font color=\"comment\">" + str(msg["record"]) + "</font>\n\
            >当前批次的延时时间: <font color=\"comment\">" + str(msg["schedule"]) + "</font>\n\
            "
        }
    }

    # 企业微信机器人发送
    bot_push(key, webhook_data)
    return None


if __name__ == '__main__':
    """
        提交参数
        --application_name SensorsAppEventTopic --active_batches 0
    """

    option_parser = option_parser()

    options, args = option_parser.parse_args(sys.argv[1:])

    if options.application_name is None or options.active_batches is None:
        print("请指定完整参数 --application_name --active_batches")
        exit(1)

    active_batch = 0
    record = ""
    schedule = ""

    # http://localhost:8088/cluster/scheduler
    # yarn resource manager url
    resource_manager_url = "http://x.x.x.x:8088/cluster/scheduler"
    resource_manager_url_html = requests.get(resource_manager_url).content.decode("utf-8")
    # print(resource_manager_url_html)

    html = etree.HTML(resource_manager_url_html)

    application_content = html.xpath('//*[@id="apps"]/script')

    for content in application_content:
        application_text_list = content.text.split("=", 1)[1].split("],")
        for application_text in application_text_list:
            application_text = application_text.replace("[", "").replace("]", "").split(",")
            application_name = application_text[2].replace("\"", "")
            application_id = re.findall(">(.*)<", str(application_text[0]))[0]

            if application_name == options.application_name:
                # spark streaming web ui
                streaming_url = "http://x.x.x.x:20888/proxy/%s/streaming/" % application_id
                streaming_html = requests.get(streaming_url).content.decode("utf-8")
                # print(streaming_html)
                s_html = etree.HTML(streaming_html)
                streaming_context_list = s_html.xpath('//span[@id="waitingBatches"]/h4/a')
                # print(streaming_context_list)

                # 清洗 active_batch
                for streaming_context in streaming_context_list:
                    active_batches = streaming_context.text
                    # print(active_batches)
                    active_batch = int(re.findall(r"\((\d*)\)", active_batches)[0])
                    # print(active_batch)
                # 说明：解析路径，spark2和spark3略有区别
                streaming_records_list = s_html.xpath('//*[@id="waitingBatches-table"]/tbody/*/td[2]')

                # 清洗 record
                for records in streaming_records_list:
                    record = records.text
                streaming_scheduling_delay_list = s_html.xpath('//*[@id="waitingBatches-table"]/tbody/*/td[3]')

                # 清洗 scheduling delay
                for scheduling in streaming_scheduling_delay_list:
                    schedule = scheduling.text

                print(active_batch)
                if active_batch > int(options.active_batches):
                    content = "任务 %s 延时了，积压批次数量为：%d，当前批次处理的记录数为: %s，当前批次的延时时间为：%s" % (application_name, active_batch, record, schedule.strip())
                    print(content)

                    # 填上对应的企业微信机器人的KEY
                    # TODO
                    wechat_key = ""
                    msg = {
                        "application_name": application_name,
                        "ip": "x.x.x.x",
                        "streaming_url": streaming_url,
                        "active_batch": active_batch,
                        "record": record,
                        "schedule": schedule.strip()
                    }
                    bot_push_markdown(wechat_key, msg)
