import json


def generate_config():
    props = {}

    # 第一层
    source_props = {}
    process_props = {}
    sink_props = {}

    # 第二层
    source_with_props = {}
    source_with_props["connector"] = "kafka"
    source_with_props["topic"] = "instagram"
    source_with_props["properties.bootstrap.servers"] = "172.16.7.116:9092"
    source_with_props["properties.group.id"] = "test"
    source_with_props["format"] = "json"
    source_with_props["properties.security.protocol"] = "SASL_PLAINTEXT"
    source_with_props["properties.sasl.mechanism"] = "PLAIN"
    source_with_props[
        "properties.sasl.jaas.config"] = "org.apache.kafka.common.security.plain.PlainLoginModule required username=\"ptreader\" password=\"pt30@123\";"
    source_with_props["scan.startup.mode"] = "earliest-offset"

    source_props["sql"] = "select * from source"
    source_props["table_name"] = "instagram"
    source_props["schema"] = "checkLocation string,message string,type string"
    source_props["with"] = source_with_props

    process_props["sql"] = "select * from process"

    sink_with_props = {}
    sink_with_props["connector"] = "elasticsearch-7"
    sink_with_props["hosts"] = "http://172.16.7.52:19200"
    sink_with_props["index"] = "lzy_test"
    sink_props["sql"] = "select * from sink"
    sink_props["table_name"] = "myUserTable"
    sink_props["schema"] = "message string"
    sink_props["with"] = sink_with_props

    props["source"] = source_props
    props["process"] = process_props
    props["sink"] = sink_props
    props["parallelism"] = 4

    return props


def save_properties(properties, path):
    """
    保存配置, properties文件格式
    :param properties 配置内容
    :param path 配置文件路径
    """
    # 保存配置到本地文件
    with open(path, 'w', encoding='utf-8') as props:
        for k, v in properties.items():
            result = str(k) + "=" + str(v) + "\n"
            props.write(result)

    return 'success'


def save_conf(properties, path):
    """
    保存配置
    :param properties 配置内容
    :param path 配置文件路径
    """
    # 保存配置到本地文件
    with open(path, 'w', encoding='utf-8') as props:
        props.write(str(properties))

    return 'success'


def generate_job_properties(nodes, lines):
    """
    生成任务配置
    """
    properties = {}

    # 外层配置
    source_props = {}
    sink_props = {}

    # 内层 with 配置
    source_with_props = {}
    sink_with_props = {}

    source_list = []
    process_list = []
    sink_list = []

    # 1.获取到对应的配置信息
    for node in nodes["nodes"]:
        if node['group'].lower().strip() == 'source':
            if node['type'].lower().strip() == 'kafka':
                source_with_props['connector'] = node['type']
                source_with_props['topic'] = node['config']['table']
                source_with_props['properties.bootstrap.servers'] = node['config']['bootstrap.servers']
                source_with_props['properties.group.id'] = node['config']['group.id']
                source_with_props['format'] = "json"
                source_with_props['properties.security.protocol'] = node['config']['max.poll.records']
                source_with_props['key.serializer'] = node['config']['key.serializer']
                source_with_props['value.serializer'] = node['config']['value.serializer']
                source_with_props['properties.sasl.jaas.config'] = node['config']['sasl.jaas.config']
                source_with_props['scan.startup.mode'] = node['config']['auto.offset.reset']
            if node['type'].lower().strip() == 'es':
                source_with_props["connector"] = node['type']
                source_with_props["hosts"] = node['config']["hosts"]
                source_with_props["index"] = node['config']["index"]
            if node['type'].lower().strip() == 'mysql':
                source_with_props["connector"] = "jdbc"
                source_with_props["url"] = node['config']["url"]
                source_with_props["driver"] = node['config']["driver"]
            if node['type'].lower().strip() == 'mongodb':
                source_with_props["connector"] = "mongodb"
                source_with_props["host"] = node['config']["host"]
                source_with_props["port"] = node['config']["port"]
                source_with_props["database"] = node['config']["database"]
                source_with_props["collection"] = node['config']["collection"]

            source_props['with'] = source_with_props
            source_props['id'] = node['id']
            source_props['table_name'] = node['config']['table']
            source_props['schema'] = node['config']['schema']

            source_list.append(source_props)
            properties[node['group']] = source_list

        if node['group'].lower().strip() == 'process':
            if node['type'].lower().strip() == 'flink sql':
                process_with_props = {'id': node['id'], 'sql': node['config']['sql'], 'table_name': node['config']['table']}

                # 有多个process，区分key group_id
                process_list.append(process_with_props)
            properties[node['group']] = process_list

        if node['group'].lower().strip() == 'sink':
            if node['type'].lower().strip() == 'kafka':
                sink_with_props['connector'] = node['type']
                sink_with_props['topic'] = node['config']['table']
                sink_with_props['properties.bootstrap.servers'] = node['config']['properties.bootstrap.servers']
                sink_with_props['properties.group.id'] = node['config']['properties.group.id']
                sink_with_props['format'] = "json"
                sink_with_props['properties.security.protocol'] = node['config']['properties.security.protocol']
                sink_with_props['properties.sasl.mechanism'] = node['config']['properties.sasl.mechanism']
                sink_with_props['properties.sasl.jaas.config'] = node['config']['properties.sasl.jaas.config']
                sink_with_props['scan.startup.mode'] = node['config']['scan.startup.mode']
            if node['type'].lower().strip() == 'elasticsearch':
                sink_with_props["connector"] = "elasticsearch-7"
                sink_with_props["hosts"] = node['config']["hosts"]
                sink_with_props["index"] = node['config']["index"]
            if node['type'].lower().strip() == 'mysql':
                sink_with_props["connector"] = "jdbc"
                sink_with_props["url"] = node['config']["url"]
                sink_with_props["driver"] = node['config']["driver"]
            if node['type'].lower().strip() == 'mongodb':
                sink_with_props["connector"] = "mongodb"
                sink_with_props["host"] = node['config']["host"]
                sink_with_props["port"] = node['config']["port"]
                sink_with_props["database"] = node['config']["database"]
                sink_with_props["collection"] = node['config']["collection"]

            sink_props['with'] = sink_with_props
            sink_props['id'] = node['id']
            sink_props['table_name'] = node['config']['table']
            sink_props['schema'] = node['config']['schema']

            sink_list.append(sink_props)
            properties[node['group']] = sink_list

    # 节点连线信息
    line_list = []
    for line in lines["lines"]:
        a = (line["from"], line["to"])
        line_list.append(a)
    # 封装连线信息
    line_seq = {'seq': line_list}
    properties['lines'] = line_seq
    # 默认并行度为2
    properties['parallelism'] = 2

    return json.dumps(properties)


def generate_job_properties2(nodes, lines):
    """
    生成任务配置
    """
    properties = {}

    # 外层配置
    source_props = {}
    sink_props = {}

    # 内层 with 配置
    source_with_props = {}
    sink_with_props = {}

    source_list = []
    process_list = []
    sink_list = []

    # 1.获取到对应的配置信息
    for node in nodes["nodes"]:
        if node['group'].lower().strip() == 'source':
            if node['type'].lower().strip() == 'kafka':
                source_with_props['connector'] = node['type']
                source_with_props['topic'] = node['config']['table']
                source_with_props['properties.bootstrap.servers'] = node['config']['bootstrap.servers']
                source_with_props['properties.group.id'] = node['config']['group.id']
                source_with_props['format'] = "json"
                source_with_props['properties.security.protocol'] = node['config']['max.poll.records']
                source_with_props['key.serializer'] = node['config']['key.serializer']
                source_with_props['value.serializer'] = node['config']['value.serializer']
                source_with_props['properties.sasl.jaas.config'] = node['config']['sasl.jaas.config']
                source_with_props['scan.startup.mode'] = node['config']['auto.offset.reset']
            if node['type'].lower().strip() == 'es':
                source_with_props["connector"] = node['type']
                source_with_props["hosts"] = node['config']["hosts"]
                source_with_props["index"] = node['config']["index"]
            if node['type'].lower().strip() == 'mysql':
                source_with_props["connector"] = "jdbc"
                source_with_props["url"] = node['config']["url"]
                source_with_props["driver"] = node['config']["driver"]
            if node['type'].lower().strip() == 'mongodb':
                source_with_props["connector"] = "mongodb"
                source_with_props["host"] = node['config']["host"]
                source_with_props["port"] = node['config']["port"]
                source_with_props["database"] = node['config']["database"]
                source_with_props["collection"] = node['config']["collection"]

            source_props['with'] = source_with_props
            source_props['id'] = node['id']
            source_props['table_name'] = node['config']['table']
            source_props['schema'] = node['config']['schema']

            source_list.append(source_props)
            properties[node['group']] = source_list

        if node['group'].lower().strip() == 'process':
            if node['type'].lower().strip() == 'flink sql':
                process_with_props = {'id': node['id'], 'sql': node['config']['sql'], 'table_name': node['config']['table']}

                # 有多个process，区分key group_id
                process_list.append(process_with_props)
            properties[node['group']] = process_list

        if node['group'].lower().strip() == 'sink':
            if node['type'].lower().strip() == 'kafka':
                sink_with_props['connector'] = node['type']
                sink_with_props['topic'] = node['config']['table']
                sink_with_props['properties.bootstrap.servers'] = node['config']['properties.bootstrap.servers']
                sink_with_props['properties.group.id'] = node['config']['properties.group.id']
                sink_with_props['format'] = "json"
                sink_with_props['properties.security.protocol'] = node['config']['properties.security.protocol']
                sink_with_props['properties.sasl.mechanism'] = node['config']['properties.sasl.mechanism']
                sink_with_props['properties.sasl.jaas.config'] = node['config']['properties.sasl.jaas.config']
                sink_with_props['scan.startup.mode'] = node['config']['scan.startup.mode']
            if node['type'].lower().strip() == 'elasticsearch':
                sink_with_props["connector"] = "elasticsearch-7"
                sink_with_props["hosts"] = node['config']["hosts"]
                sink_with_props["index"] = node['config']["index"]
            if node['type'].lower().strip() == 'mysql':
                sink_with_props["connector"] = "jdbc"
                sink_with_props["url"] = node['config']["url"]
                sink_with_props["driver"] = node['config']["driver"]
            if node['type'].lower().strip() == 'mongodb':
                sink_with_props["connector"] = "mongodb"
                sink_with_props["host"] = node['config']["host"]
                sink_with_props["port"] = node['config']["port"]
                sink_with_props["database"] = node['config']["database"]
                sink_with_props["collection"] = node['config']["collection"]

            sink_props['with'] = sink_with_props
            sink_props['id'] = node['id']
            sink_props['table_name'] = node['config']['table']
            sink_props['schema'] = node['config']['schema']

            sink_list.append(sink_props)
            properties[node['group']] = sink_list

    # 节点连线信息
    line_list = []
    for line in lines["lines"]:
        a = (line["from"], line["to"])
        line_list.append(a)
    # 封装连线信息
    line_seq = {'seq': line_list}
    properties['lines'] = line_seq
    # 默认并行度为2
    properties['parallelism'] = 2

    return json.dumps(properties)


if __name__ == "__main__":
    # prop = generate_config()
    # print(prop)
    #
    # result = save_conf(prop, "/props.properties")
    # print(result)

    nodes = {
        "nodes": [
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
    }

    lines = {
        "lines": [
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
    }

    properties = generate_job_properties(nodes,lines)
    print(properties)
