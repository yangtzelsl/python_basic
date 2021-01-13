#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

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
    sasl_plain_username=PRODUCER_SASL_PLAIN_PASSWORD,
    sasl_plain_password=PRODUCER_SASL_PLAIN_PASSWORD
)

# 构造数据
msg_dict = {
    "id": 1238123899121,
    "name": "asdlkjasjkdla998y1122",
    "date1": "1990-10-14",
    "obj1": {
        "time1": "12:12:43",
        "str1": "sfasfafs",
        "long1": 2324342345
    },
    "arr1": [
        {
            "f1": "f1str11",
            "f2": 134
        },
        {
            "f1": "f1str22",
            "f2": 555
        }
    ],
    "time1": "12:12:43Z",
    "timestamp1": "1990-10-14T12:12:43Z",
    "map1": {
        "flink": 123
    },
    "mapinmap": {
        "inner_map": {
            "key1": 234
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
msg = json.dumps(msg_dict1, ensure_ascii=False)

topic = "flink_type"

# 发送消息
producer.send(topic, value=str.encode(msg))
producer.flush()
print("消息发送完毕: " + str(msg_dict1))

# 关闭资源
producer.close()
