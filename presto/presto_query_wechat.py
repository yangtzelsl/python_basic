# -*- coding:UTF-8 -*-

import json

import prestodb
import requests

"""
# 使用venv创建虚拟环境（注意和virtualenv的区别）
python3 -m venv virtualName

# 激活虚拟环境
source virtualName/bin/active

# 查看虚拟环境默认python版本
python --version

# 安装依赖
pip install presto-python-client

# 执行脚本
python3 presto_query_wechat.py
"""

HOST = 'x.x.x.x'
PORT = 8889
USER = 'user'
CATALOG = 'hive'
SCHEMA = 'default'
HTTP_SCHEMA = 'http'


def get_data_from_presto(sql):
    conn = prestodb.dbapi.connect(
        host=HOST,  # host位置
        port=PORT,  # 端口位置
        user=USER,  # 用户名
        catalog=CATALOG,  # 使用的hive
        schema=SCHEMA,  # 使用的schema，默认是default，可以不改
        http_scheme=HTTP_SCHEMA  # 后面的暂时不添加，http的添加后报错,
        # auth=prestodb.auth.BasicAuthentication("", "")
    )
    conn._http_session.verify = './presto.pem'  # 校验文件存储位置，这个应该是默认位置
    cur = conn.cursor()
    cur.execute(sql)  # sql语句
    rows = cur.fetchall()
    print(rows)
    return rows


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


def bot_push_text(key, msg):
    """
    发送文本格式的消息
    """
    webhook_data = {
        "msgtype": "text",
        "text": {
            "content": msg
        }
    }

    # 企业微信机器人发送
    bot_push(key, webhook_data)
    return None


def bot_push_markdown(key, msg):
    """
    发送markdown格式的消息
    """
    webhook_data = {
        "msgtype": "markdown",
        "markdown": {
            "content": "\
            <font color=\"warning\">神策dws数据统计，请相关同事注意。</font>\n\
            >查询日期: <font color=\"comment\">" + msg["date"] + "</font>\n\
            >注册用户数量: <font color=\"comment\">" + str(msg["count"]) + "</font>\n\
            "
        }
    }

    # 企业微信机器人发送
    bot_push(key, webhook_data)
    return None


def bot_push_image(key, data64, md5):
    """
    发送图片格式的消息
    """
    webhook_data = {
        "msgtype": "image",
        "image": {
            "base64": data64,
            "md5": md5
        }
    }
    # 企业微信机器人发送
    bot_push(key, webhook_data)
    return None


if __name__ == '__main__':
    # wechat robot key
    wechat_key = ""

    # 要执行的sql语句
    sql = '''
    select  date ,count(distinct  distinct_id) as n  
    from table_name 
    where date>='2021-08-01' and event in ('RegisterResult') and  error_code = 0
    group by date
    order by date desc
    limit 1
    '''

    # 查询数据
    results = get_data_from_presto(sql=sql)

    # 构造消息
    msg = {
        "date": results[0][0],
        "count": results[0][1]
    }

    # 发送机器人
    bot_push_markdown(wechat_key, msg)
