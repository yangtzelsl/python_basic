import json

j1 = {
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

# j1 = json.loads(s1)
j2 = {"source": [], "process": [], "sink": []}
for value in j1.get("nodes", {}):
    if value.get("group", "") == "source":
        j2.get("source", []).append(value)
    elif value.get("group", "") == "process":
        j2.get("process", []).append(value)
    elif value.get("group", "") == "sink":
        j2.get("sink", []).append(value)
        # print(j2)
print(json.dumps(j2, ensure_ascii=False))

properties = {}
for k in j2.keys():
    nodes = j2.get(k, [])

    for node in nodes:
        inner_list = []
        with_props = {}
        props = {}
        if node['group'].lower().strip() == 'source':
            if node['type'].lower().strip() == 'kafka':
                with_props['connector'] = node['type']
                with_props['topic'] = node['config']['table']
                with_props['properties.bootstrap.servers'] = node['config']['bootstrap.servers']
                with_props['properties.group.id'] = node['config']['group.id']
                with_props['format'] = "json"
                with_props['properties.security.protocol'] = node['config']['max.poll.records']
                with_props['key.serializer'] = node['config']['key.serializer']
                with_props['value.serializer'] = node['config']['value.serializer']
                with_props['properties.sasl.jaas.config'] = node['config']['sasl.jaas.config']
                with_props['scan.startup.mode'] = node['config']['auto.offset.reset']
            if node['type'].lower().strip() == 'es':
                with_props["connector"] = node['type']
                with_props["hosts"] = node['config']["hosts"]
                with_props["index"] = node['config']["index"]
            if node['type'].lower().strip() == 'mysql':
                with_props["connector"] = "jdbc"
                with_props["url"] = node['config']["url"]
                with_props["driver"] = node['config']["driver"]
            if node['type'].lower().strip() == 'mongodb':
                with_props["connector"] = "mongodb"
                with_props["host"] = node['config']["host"]
                with_props["port"] = node['config']["port"]
                with_props["database"] = node['config']["database"]
                with_props["collection"] = node['config']["collection"]

            props['with'] = with_props
            props['id'] = node['id']
            props['table_name'] = node['config']['table']
            props['schema'] = node['config']['schema']

            inner_list.append(props)
            properties[node['group']] = inner_list

        if node['group'].lower().strip() == 'process':
            if node['type'].lower().strip() == 'flink sql':
                with_props = {'id': node['id'], 'sql': node['config']['sql'],
                              'table_name': node['config']['table']}

                # 有多个process，区分key group_id
                inner_list.append(with_props)
                properties[node['group']] = inner_list

        if node['group'].lower().strip() == 'sink':
            if node['type'].lower().strip() == 'kafka':
                with_props['connector'] = node['type']
                with_props['topic'] = node['config']['table']
                with_props['properties.bootstrap.servers'] = node['config']['properties.bootstrap.servers']
                with_props['properties.group.id'] = node['config']['properties.group.id']
                with_props['format'] = "json"
                with_props['properties.security.protocol'] = node['config']['properties.security.protocol']
                with_props['properties.sasl.mechanism'] = node['config']['properties.sasl.mechanism']
                with_props['properties.sasl.jaas.config'] = node['config']['properties.sasl.jaas.config']
                with_props['scan.startup.mode'] = node['config']['scan.startup.mode']
            if node['type'].lower().strip() == 'elasticsearch':
                with_props["connector"] = "elasticsearch-7"
                with_props["hosts"] = node['config']["hosts"]
                with_props["index"] = node['config']["index"]
            if node['type'].lower().strip() == 'mysql':
                with_props["connector"] = "jdbc"
                with_props["url"] = node['config']["url"]
                with_props["driver"] = node['config']["driver"]
            if node['type'].lower().strip() == 'mongodb':
                with_props["connector"] = "mongodb"
                with_props["host"] = node['config']["host"]
                with_props["port"] = node['config']["port"]
                with_props["database"] = node['config']["database"]
                with_props["collection"] = node['config']["collection"]

            props['with'] = with_props
            props['id'] = node['id']
            props['table_name'] = node['config']['table']
            props['schema'] = node['config']['schema']

            inner_list.append(props)
            properties[node['group']] = inner_list

print(json.dumps(properties, ensure_ascii=False))
