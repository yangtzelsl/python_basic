from hdfs.client import InsecureClient
from settings import *


def read_hdfs_file(client, filename):
    """
    读取hdfs文件内容,将每行存入数组返回
    :param client:
    :param filename:
    :return:
    """
    lines = []
    with client.read(filename, encoding='utf-8', delimiter='\n') as reader:
        for line in reader:
            lines.append(line.strip())
    return lines


def mkdirs(client, hdfs_path):
    """
    创建目录
    :param client:
    :param hdfs_path:
    :return:
    """
    client.makedirs(hdfs_path)


def delete_hdfs_file(client, hdfs_path):
    """
    删除hdfs文件
    :param client:
    :param hdfs_path:
    :return:
    """
    client.delete(hdfs_path)


def put_to_hdfs(client, local_path, hdfs_path):
    """
    上传文件到hdfs
    :param client:
    :param local_path:
    :param hdfs_path:
    :return:
    """
    client.upload(hdfs_path, local_path, cleanup=True)


def get_from_hdfs(client, hdfs_path, local_path):
    """
    从hdfs获取文件到本地
    :param client:
    :param hdfs_path:
    :param local_path:
    :return:
    """
    client.download(hdfs_path, local_path, overwrite=False)


def append_to_hdfs(client, hdfs_path, data):
    """
    追加数据到hdfs文件
    :param client:
    :param hdfs_path:
    :param data:
    :return:
    """
    client.write(hdfs_path, data, overwrite=False, append=True, encoding='utf-8')


def write_to_hdfs(client, hdfs_path, data):
    """
    覆盖数据写到hdfs文件
    :param client:
    :param hdfs_path:
    :param data:
    :return:
    """
    client.write(hdfs_path, data, overwrite=True, append=False, encoding='utf-8')


def move_or_rename(client, hdfs_src_path, hdfs_dst_path):
    """
    移动或者修改文件
    :param client:
    :param hdfs_src_path:
    :param hdfs_dst_path:
    :return:
    """
    client.rename(hdfs_src_path, hdfs_dst_path)


def list(client, hdfs_path):
    """
    返回目录下的文件
    :param client:
    :param hdfs_path:
    :return:
    """
    return client.list(hdfs_path, status=False)


if __name__ == '__main__':
    # 路径定义
    local_path = '/test.properties'
    hdfs_path = '/user/flink/test.properties'

    properties_json = {
        "config": {
            "source": [
                {
                    "with": {
                        "connector": "kafka",
                        "topic": "instagram",
                        "bootstrap.servers": "172.16.7.10:9092,172.16.7.11:9092,172.16.7.12:9092",
                        "group.id": "flink_facebook_data_quality",
                        "format": "json"
                    },
                    "id": "nodeA",
                    "table_name": "instagram",
                    "schema": "checkLocation string, message string, type string"
                }
            ],
            "process": [
                {
                    "id": "nodeB",
                    "sql": "slect xx",
                    "table_name": "aaa"
                },
                {
                    "id": "nodeB1",
                    "sql": "slect xx",
                    "table_name": "bbb"
                },
                {
                    "id": "nodeB2",
                    "sql": "slect xx",
                    "table_name": "ccc"
                }
            ],
            "sink": [
                {
                    "with": {
                        "format": "json",
                        "connector": "elasticsearch-7",
                        "hosts": "http://172.16.7.52:19200",
                        "index": "lzy_test"
                    },
                    "id": "nodeC",
                    "table_name": "myUserTable",
                    "schema": "message string"
                }
            ],
            "lines": {
                "seq": [
                    [
                        "nodeA",
                        "nodeB"
                    ],
                    [
                        "nodeB",
                        "nodeB1"
                    ],
                    [
                        "nodeB",
                        "nodeB2"
                    ],
                    [
                        "nodeB1",
                        "nodeC"
                    ],
                    [
                        "nodeB2",
                        "nodeC"
                    ]
                ]
            },
            "parallelism": 2
        },
        "parallelism": 2
    }

    # The address and the base port where the dfs namenode web ui will listen on.
    # client = Client("http://172.16.7.59:9870",root='/user/flink')
    client = InsecureClient(HDFS_CLIENT_URI, user=HDFS_DEFAULT_USER)

    # 1.显示目录下的所有文件
    # list_dir = list(client, hdfs_path)
    # print(list_dir)

    # 2.创建目录
    # mkdirs(client,'/input/python')

    # 3.上传文件
    # put_to_hdfs(client, local_path, hdfs_path)

    # 4.读文件
    # read_hdfs_file(client,'/input/emp.csv')

    # 5.追加文件
    # append_to_hdfs(client,'/input/emp.csv','我爱你'+'\n')

    # 6.覆盖写文件
    import json

    write_to_hdfs(client, hdfs_path, "")
    for key in properties_json.keys():
        print(json.dumps(json.dumps(properties_json[key]), indent=4, ensure_ascii=False)[1:-1])
        append_to_hdfs(client, hdfs_path,
                       key + "=" + json.dumps(json.dumps(properties_json[key]), indent=4, ensure_ascii=False)[
                                   1:-1] + "\n")

    # 7.移动文件或重命名
    # move_or_rename(client,'/input/2.csv', '/input/emp.csv')

    # 8.修改文件所属用户组
    # chown(client,'/input/1.csv', 'root')
