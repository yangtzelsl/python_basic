# -*- coding: utf-8 -*-
from kafka import KafkaConsumer

from settings import *

consumer = KafkaConsumer(TOPIC,
                         group_id=GROUP_ID,
                         bootstrap_servers=BOOTSTRAP_SERVERS,
                         auto_offset_reset=AUTO_OFFSET_RESET,
                         security_protocol=SECURITY_PROTOCOL,
                         sasl_mechanism=SASL_MECHANSIM,
                         sasl_plain_username=CONSUMER_SASL_PLAIN_USERNAME,
                         sasl_plain_password=CONSUMER_SASL_PLAIN_PASSWORD
                         )
for msg in consumer:
    recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
    print(recv)
