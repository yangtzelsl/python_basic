# -*- coding: utf-8 -*-
from kafka import KafkaConsumer
import json

from settings import *

consumer = KafkaConsumer(TOPIC,
                         group_id=GROUP_ID,
                         bootstrap_servers=BOOTSTRAP_SERVERS,
                         auto_offset_reset=AUTO_OFFSET_RESET,
                         security_protocol=SECURITY_PROTOCOL,
                         sasl_mechanism=SASL_MECHANISM,
                         sasl_plain_username=CONSUMER_SASL_PLAIN_USERNAME,
                         sasl_plain_password=CONSUMER_SASL_PLAIN_PASSWORD
                         )
for msg in consumer:
    recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
    # 将消息转化为字符串格式(byte -> str)
    message = str(msg.value, 'utf-8')
    # 数据JSON化，便于取值
    json_message = json.loads(str(msg.value, 'utf-8'))
    # 只拿 pro 生产
    if json_message['project_id'] == 5:
        print(message)