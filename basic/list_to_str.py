import json


def generate_job_properties2(nodes, lines):
    """
    生成任务配置
    :param nodes:
    :param lines:
    :return:
    """
    # 转换获取到的nodes节点格式
    j2 = {"source": [], "process": [], "sink": []}
    for value in nodes:
        if value.get("group", "") == "source":
            j2.get("source", []).append(value)
        elif value.get("group", "") == "process":
            j2.get("process", []).append(value)
        elif value.get("group", "") == "sink":
            j2.get("sink", []).append(value)

    # 结果配置
    result = {"source": [], "process": [], "sink": []}
    for key in j2.keys():
        inner_list = []
        if key == "source":
            for node in j2.get(key):
                inner_dict = {}
                with_dict = {}
                if node['type'].lower().strip() == 'kafka':
                    with_dict['connector'] = node['type']
                    with_dict['topic'] = node['config']['table']
                    with_dict['bootstrap.servers'] = node['config']['bootstrap.servers']
                    with_dict['group.id'] = node['config']['group.id']
                    with_dict['format'] = "json"
                if node['type'].lower().strip() == 'es' or node['type'].lower().strip() == 'elasticsearch':
                    with_dict["connector"] = 'elasticsearch-7'
                    with_dict["hosts"] = node['config']["hosts"]
                    with_dict["index"] = node['config']["index"]
                if node['type'].lower().strip() == 'mysql':
                    with_dict["connector"] = "jdbc"
                    with_dict["url"] = node['config']["url"]
                    with_dict["driver"] = node['config']["driver"]
                if node['type'].lower().strip() == 'mongodb':
                    with_dict["connector"] = "mongodb"
                    with_dict["host"] = node['config']["host"]
                    with_dict["port"] = node['config']["port"]
                    with_dict["database"] = node['config']["database"]
                    with_dict["collection"] = node['config']["collection"]
                inner_dict["with"] = with_dict
                inner_dict["id"] = node['id']
                inner_dict["table_name"] = node['config']['table']
                inner_dict['schema'] = node['config']['schema']

                inner_list.append(inner_dict)
            result["source"] = inner_list
        elif key == "process":
            for node in j2.get(key):
                inner_dict = {}
                if node['type'].lower().strip() == 'flink sql':
                    inner_dict = {'id': node['id'], 'sql': node['config']['sql'],
                                  'table_name': node['config']['table']}
                    # 有多个process，区分key group_id
                    inner_list.append(inner_dict)
            result["process"] = inner_list
        elif key == "sink":
            for node in j2.get(key):
                inner_dict = {}
                with_dict = {}
                if node['type'].lower().strip() == 'kafka':
                    with_dict['connector'] = node['type']
                    with_dict['topic'] = node['config']['table']
                    with_dict['bootstrap.servers'] = node['config']['bootstrap.servers']
                    with_dict['group.id'] = node['config']['group.id']
                    with_dict['format'] = "json"
                if node['type'].lower().strip() == 'es' or node['type'].lower().strip() == 'elasticsearch':
                    with_dict["connector"] = 'elasticsearch-7'
                    with_dict["hosts"] = node['config']["hosts"]
                    with_dict["index"] = node['config']["index"]
                if node['type'].lower().strip() == 'mysql':
                    with_dict["connector"] = "jdbc"
                    with_dict["url"] = node['config']["url"]
                    with_dict["driver"] = node['config']["driver"]
                if node['type'].lower().strip() == 'mongodb':
                    with_dict["connector"] = "mongodb"
                    with_dict["host"] = node['config']["host"]
                    with_dict["port"] = node['config']["port"]
                    with_dict["database"] = node['config']["database"]
                    with_dict["collection"] = node['config']["collection"]
                inner_dict["with"] = with_dict
                inner_dict["id"] = node['id']
                inner_dict["table_name"] = node['config']['table']
                inner_dict['schema'] = node['config']['schema']

                inner_list.append(inner_dict)
            result["sink"] = inner_list

    # 节点连线信息
    line_list = []
    for line in lines:
        a = (line["from"], line["to"])
        line_list.append(a)
    # 封装连线信息
    line_seq = {'seq': line_list}
    result['lines'] = line_seq
    # 默认并行度为2
    result['parallelism'] = 2
    return result


if __name__ == "__main__":
    nodes = [
        {
            "id": "nodeA",
            "name": "节点A-不可拖拽",
            "job_id": "6",
            "group": "source",
            "type": "kafka",
            "left": "18px",
            "top": "223px",
            "ico": "el-icon-user-solid",
            "state": "success",
            "config": {
                "table": "instagram",
                "schema": "checkLocation string,message string,type string, primarykey",
                "group.id": "flink_facebook_data_quality",
                "bootstrap.servers": "172.16.7.10:9092,172.16.7.11:9092,172.16.7.12:9092",
                "max.poll.records": "10000",
                "key.serializer": "org.apache.kafka.common.serialization.StringSerializer",
                "value.serializer": "org.apache.kafka.common.serialization.StringSerializer",
                "sasl.jaas.config": "org.apache.kafka.common.security.plain.PlainLoginModule required username='ptreader' password='pt30@123';",
                "auto.offset.reset": "earliest"
            }
        },
        {
            "id": "nodeB",
            "name": "节点B-不可拖拽",
            "job_id": "6",
            "group": "process",
            "type": "flink sql",
            "left": "18px",
            "top": "223px",
            "ico": "el-icon-user-solid",
            "state": "success",
            "config": {
                "sql": "slect xx",
                "table": "aaa"
            }
        },
        {
            "id": "nodeB1",
            "name": "节点B-不可拖拽",
            "job_id": "6",
            "group": "process",
            "type": "flink sql",
            "left": "18px",
            "top": "223px",
            "ico": "el-icon-user-solid",
            "state": "success",
            "config": {
                "sql": "slect xx",
                "table": "bbb"
            }
        },
        {
            "id": "nodeB2",
            "name": "节点B-不可拖拽",
            "job_id": "6",
            "group": "process",
            "type": "flink sql",
            "left": "18px",
            "top": "223px",
            "ico": "el-icon-user-solid",
            "state": "success",
            "config": {
                "sql": "slect xx",
                "table": "ccc"
            }
        },
        {
            "id": "nodeC",
            "name": "节点C-不可拖拽",
            "job_id": "6",
            "group": "sink",
            "type": "elasticsearch",
            "left": "18px",
            "top": "223px",
            "ico": "el-icon-user-solid",
            "state": "success",
            "config": {
                "table": "myUserTable",
                "schema": "message string",
                "hosts": "http://172.16.7.52:19200",
                "index": "lzy_test"
            }
        }
    ]

    lines = [
        {
            "from": "nodeA",
            "to": "nodeB"
        },
        {
            "from": "nodeB",
            "to": "nodeB1"
        },
        {
            "from": "nodeB",
            "to": "nodeB2"
        },
        {
            "from": "nodeB1",
            "to": "nodeC"
        },
        {
            "from": "nodeB2",
            "to": "nodeC"
        }
    ]

    # for node in nodes:
    #     print(node)
    #     print(type(node))


    result = generate_job_properties2(nodes, lines)
    print(json.dumps(result))
