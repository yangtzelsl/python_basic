import logging

import requests

from settings import *

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
    print(type(result), result, sep='\n')
