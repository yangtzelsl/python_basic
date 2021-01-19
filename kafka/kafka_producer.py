#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json
import random
import string
import time

from kafka import KafkaProducer

from settings import *

# 参数配置
producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    acks=ACKS,
    retries=0,
    batch_size=16384,
    max_block_ms=6000,
    request_timeout_ms=4000,
    security_protocol=SECURITY_PROTOCOL,
    sasl_mechanism=SASL_MECHANSIM,
    sasl_plain_username=PRODUCER_SASL_PLAIN_USERNAME,
    sasl_plain_password=PRODUCER_SASL_PLAIN_PASSWORD
)

# 构造数据
msg_dict = {
    "id": random.randint(1000, 9999),
    "name": ''.join(random.sample(string.ascii_letters + string.digits, 8)),
    "date1": (datetime.datetime.now() + datetime.timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d"),
    "obj1": {
        "time1": time.strftime("%H:%M:%S", time.localtime()),
        "str1": "sfasfafs",
        "long1": 2324342345
    },
    "arr1": [
        {
            "f1": "f1str11",
            "f2": random.randint(0, 9)
        },
        {
            "f1": "f1str22",
            "f2": random.randint(0, 100)
        }
    ],
    "time1": time.strftime("%H:%M:%S", time.localtime()),
    "timestamp1": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    "map1": {
        "flink": random.randint(10, 1000)
    },
    "mapinmap": {
        "inner_map": {
            "key1": random.randint(2, 8)
        }
    }
}
msg_dict1 = {
    "id": 1238123899121,
    "obj1": {
        "time1": "12:12:43",
        "str1": "sfasfafs",
        "long1": 2324342345
    }
}
msg_dict2 = {
    "id": random.randint(1000, 9999),
    "name": ''.join(random.sample(string.ascii_letters + string.digits, 8)),
    "date1": (datetime.datetime.now() + datetime.timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d"),
    "obj1": {
        "time1": time.strftime("%H:%M:%S", time.localtime()),
        "str1": "sfasfafs",
        "long1": 2324342345
    },
    "time1": time.strftime("%H:%M:%S", time.localtime()),
    "timestamp1": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    "map1": {
        "flink": random.randint(10, 1000)
    }
}
msg = json.dumps(msg_dict2, ensure_ascii=False)

topic = "flink_type"

# 发送消息
producer.send(topic, value=str.encode(msg))
producer.flush()
print("消息发送完毕: " + str(msg_dict2))

# 关闭资源
producer.close()
