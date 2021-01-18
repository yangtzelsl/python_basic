import logging

import requests

from settings import *
import os

cur_path = os.path.dirname(os.path.realpath(__file__))  # log_path是存放日志的路径
log_path = os.path.join(os.path.dirname(cur_path), 'logs')
if not os.path.exists(log_path):
    os.mkdir(log_path)  # 如果不存在这个logs文件夹，就自动创建一个

logger = logging.getLogger(__name__)

URL = 'http://ip.taobao.com/service/getIpInfo.php'  # 淘宝IP地址库API
try:
    r = requests.get(URL, params={'ip': '8.8.8.8'}, timeout=1)
    r.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
except requests.ConnectionError as e:
    logging.error(ConnectionError + str(e))
except requests.HTTPError as e:
    logging.error(HTTPError + str(e))
else:
    result = r.json()
    logger.info(result)
    print(type(result), result, sep='\n')
