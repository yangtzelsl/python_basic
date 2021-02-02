# -*- coding: utf-8 -*-
# Version: 1.0.0
# Description: py_Hive2Kafka2kafka
# Author: wqbin
# Create_date:20191026

import datetime
import logging
import os
import random
import re
import string
import subprocess as sp
import sys
import time
from logging import handlers

from kafka import KafkaProducer
from pyhs2.haconnection import HAConnection

################################环境变量的设置############################################
# 1.指定编码格式
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

# 2.加载fi的环境变量
ENV_FILE = '/home/root/ficlient/bigdata_env'

# 加载ENV_FILE 相当于source /home/root/ficlient/bigdata_env
proc = sp.Popen(['bash', '-c', 'source {0} && env'.format(ENV_FILE)], stdout=sp.PIPE)
for tup in map(lambda s: s.strip().split('=', 1), proc.stdout):
    k = tup[0].strip()
    v = tup[1].strip()
    os.environ[k] = v

# 3.KERBEROS 认证
KERBEROS_USER = "rootuser"
KERBEROS_KEYTAB = "/home/root/rootuser.keytab"
TGT_PATH = "/home/root/tagidentity.tgt"
os.environ['KRB5CCNAME'] = TGT_PATH
os.system("kinit -kt %s %s" % (KERBEROS_KEYTAB, KERBEROS_USER))

# 4.脚本路径 日志路径 配置路径
# MAIN_PATH = os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
MAIN_PATH = "/ETL/pybin/py_Hive2Kafka"

LOG_PATH = MAIN_PATH + "/log"
CONF_PATH = MAIN_PATH + "/conf"
# 5.参数1：批次时间 20180721
batch_date = sys.argv[1]

################################日志######################################################
# 日志中的时间格式
ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'

# 日志路径
logfile = "%s/%s.log" % (LOG_PATH, batch_date)

# 整合层日志
LOGGER = logging.getLogger("data_life_manager")

LOGGER_HANDLER = logging.handlers.RotatingFileHandler(logfile, maxBytes=20 * 1024 * 1024, backupCount=10)
FORMATTER = logging.Formatter("\r%(asctime)s [%(levelname)s] %(message)s", ISOTIMEFORMAT)
LOGGER_HANDLER.setFormatter(FORMATTER)

LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(LOGGER_HANDLER)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(FORMATTER)
LOGGER.addHandler(console)
logger = LOGGER
logger.info(MAIN_PATH)


###################################从配置文件中获取配置###################################

def get_conf(conf_file):
    """
    Get conf from a file having attribute which relatives by equal sign.
    Then, it will create and return  a dic with conf.
    """
    conf = {}

    def add_conf(key, value):
        conf[key] = value

    map(lambda _: add_conf(_[0:_.index('=')], _[_.index('=') + 1:]),
        map(lambda _: _.replace('"', '').replace('\n', ''),
            # 获取有效的配置行
            filter(lambda _: "=" in _ and not _.startswith('#'),
                   open(conf_file).readlines()
                   )
            )
        )
    return conf


db_config = get_conf(MAIN_PATH + '/conf/database.conf')

# Hive连接配置
HIVE_HOSTS = db_config.get('HIVE_HOSTS').split(',')
HIVE_PORT = db_config.get('HIVE_PORT')
queue_name = db_config.get('QUEUE_NAME')

###################################连接hive执行sql###################################
# 查询统计结果sql
sql = ''
if batch_date[6:8] == '03':
    print('batch_date[6:7]:%s' % batch_date[6:8])
    sql = "select column1, column2, column3, column4 from table1 where batch_date=%s ;" % (batch_date)
else:
    print('batch_date[6:7]:%s' % batch_date[6:8])
    sql = "select column1,column2   from table1 where batch_date=%s ;" % (batch_date)
database = "dt"
templatecode = "001"
transcode = "002"
orsenderid = "003"
orsenderchannel = "004"


def select_hive(queue_name, database, sql, logger):
    v_queue_name = "set mapred.job.queue.name=%s" % queue_name
    v_database = "use %s" % database
    sql = sql.encode('UTF-8')
    v_sql = re.sub(r';$', '', sql)
    timeout11 = 3 * 60 * 60 * 1000
    conf = {"krb_host": "hadoop001", "krb_service": "hive"}
    print(v_queue_name)
    print(v_database)
    print(v_sql)
    try:
        with HAConnection(hosts=HIVE_HOSTS,
                          port=HIVE_PORT,
                          timeout=timeout11,
                          authMechanism="KERBEROS",
                          user='rootuser',
                          configuration=conf) as haConn:
            with haConn.getConnection() as conn:
                with conn.cursor() as cur:
                    print(v_queue_name)
                    logger.info(v_queue_name)
                    cur.execute(v_queue_name)
                    print(v_database)
                    logger.info(v_database)
                    cur.execute(v_database)
                    print(v_sql)
                    logger.info(v_sql)
                    cur.execute(v_sql)
                    tuple_dic = cur.fetchall()
                    if len(tuple_dic) == 0:
                        tuple_dic = None
    except Exception as e:
        logger.error(e)
        raise Exception(e)
    return tuple_dic


####################################自定义异常类###################################

class UserDefException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


####################################拼接json字符串 发送kafka方法###################################

def send_json_to_Kafka(batch_date):
    data_cnt_tuple_dic = select_hive(queue_name, database, sql, logger)
    print(data_cnt_tuple_dic)

    list = []
    try:
        for a in data_cnt_tuple_dic:
            if len(a) == 2:
                list.append(a[0])
                list.append(a[1])
                break
            elif len(a) == 4:
                list.append(a[0])
                list.append(a[1])
                list.append(a[2])
                list.append(a[3])
                break
            else:
                raise UserDefException("select返回不是4也不是2")
    except Exception as e:
        list = []
        logger.error(e)
    print(list)

    orSenderSN = ''.join(random.sample(string.ascii_letters + string.digits, 22))
    agentSerialNo = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    verison_name = "abc"
    model_plat = "1"

    msg_head = '{"TemplateCode":"%s","TransCode":"%s","orSenderID":"%s","orSenderChannel":"%s","orSenderSN":"%s",' \
               '"orSenderDate":"%s","curTime":"%d","agentSerialNo":"%s"}' \
               % (templatecode, transcode, orsenderid, orsenderchannel, orSenderSN,
                  time.strftime("%Y%m%d", time.localtime()), int(round(time.time() * 1000)), agentSerialNo)
    start_time = batch_date
    end_time = batch_date
    if batch_date[6:8] == '03':
        end_time = datetime.datetime.combine(
            datetime.date(int(batch_date[0:4]), int(batch_date[4:6]), int(batch_date[6:8])) - datetime.timedelta(
                days=30), datetime.time.min).strftime("%Y%m%d")
    try:

        if batch_date[6:8] == '03':
            msg_result = '{' \
                         '"%s":%s,' \
                         '"%s":%s,' \
                         '"%s":%s,' \
                         '"%s":%s' \
                         '}' % ("column1", list[0], "column2", list[1], "column3", list[2], "column4", list[3])
        elif batch_date[6:8] != '03':
            msg_result = '{' \
                         '"%s":%s,' \
                         '"%s":%s' \
                         '}' % ("column1", list[0], "column2", list[1])
        else:
            raise UserDefException("select返回不是4也不是2")
    except Exception as e:
        logger.error(e)
        raise Exception(e)

    msg_body = '{"verison_name":"%s","version":"","model_plat":"%s","event_start_tm":"%s","event_end_tm":"%s","result":%s}' \
               % (verison_name, model_plat, start_time, end_time, str(msg_result).replace("'", '"'))
    msg = '{"head":%s,"body":%s}' % (msg_head, msg_body)
    logger.info(msg)

    try:
        send_kafka(msg)
    except Exception as e:
        logger.error(e)
        raise Exception(e)


bootstrap_servers = '192.168.164.202:9092,192.168.164.203:9092,192.168.164.204:9092'
topic = 'topic1'
retries = 2


# 发送数据到kafka
def send_kafka(msg):
    try:
        producer = KafkaProducer(bootstrap_servers=bootstrap_servers, retries=retries)
    except Exception as e:
        logger.error(e)
        raise Exception("catch an exception when create KafkaProducer")
    try:
        producer.send(topic, msg)
        producer.flush()
        producer.close()

    except Exception as e:
        logger.error(e)
        if producer:
            producer.close()
        raise Exception("catch an exception when send message:%s" % msg)


if __name__ == '__main__':
    send_json_to_Kafka(batch_date)
    print("data from hive to kafka has all successed")
