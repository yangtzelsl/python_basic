dict_demo = {
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
    ],
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

properties = {}

source_props = {}
sink_props = {}

source_with_props = {}
sink_with_props = {}

for node in dict_demo["nodes"]:
    if node['group'] == 'source':
        if node['type'] == 'kafka':
            source_with_props['connector'] = node['type']
            source_with_props['topic'] = node['config']['table']
            source_with_props['properties.bootstrap.servers'] = node['config']['bootstrap.servers']
            source_with_props['properties.group.id'] = node['config']['group.id']
            source_with_props['properties.security.protocol'] = node['config']['max.poll.records']
            source_with_props['key.serializer'] = node['config']['key.serializer']
            source_with_props['value.serializer'] = node['config']['value.serializer']
            source_with_props['properties.sasl.jaas.config'] = node['config']['sasl.jaas.config']
            source_with_props['scan.startup.mode'] = node['config']['auto.offset.reset']
        if node['type'] == 'elasticsearch':
            source_with_props["connector"] = node['type']
            source_with_props["hosts"] = node['config']["hosts"]
            source_with_props["index"] = node['config']["index"]

        source_props['with'] = source_with_props
        source_props['id'] = node['id']
        source_props['table_name'] = node['config']['table']
        source_props['schema'] = node['config']['schema']

        properties[node['group']] = source_props
    if node['group'] == 'process':
        if node['type'] == 'flink sql':
            process_props = {}
            process_props['id'] = node['id']
            process_props['sql'] = node['config']['sql']
            process_props['table_name'] = node['config']['table']

            properties[node['group'] + "_" + node['id']] = process_props
    if node['group'] == 'sink':
        if node['type'] == 'kafka':
            sink_with_props['connector'] = node['type']
            sink_with_props['topic'] = node['config']['table']
            sink_with_props['properties.bootstrap.servers'] = node['config']['properties.bootstrap.servers']
            sink_with_props['properties.group.id'] = node['config']['properties.group.id']
            sink_with_props['format'] = node['config']['format']
            sink_with_props['properties.security.protocol'] = node['config']['properties.security.protocol']
            sink_with_props['properties.sasl.mechanism'] = node['config']['properties.sasl.mechanism']
            sink_with_props['properties.sasl.jaas.config'] = node['config']['properties.sasl.jaas.config']
            sink_with_props['scan.startup.mode'] = node['config']['scan.startup.mode']
        if node['type'] == 'elasticsearch':
            sink_with_props["connector"] = node['type']
            sink_with_props["hosts"] = node['config']["hosts"]
            sink_with_props["index"] = node['config']["index"]

        sink_props['with'] = sink_with_props
        sink_props['id'] = node['id']
        sink_props['table_name'] = node['config']['table']
        sink_props['schema'] = node['config']['schema']

        properties[node['group']] = sink_props

line_list = []
for line in dict_demo["lines"]:
    a = (line["from"], line["to"])
    line_list.append(a)

line_seq = {}
line_seq['seq'] = line_list
properties['lines'] = line_seq
properties['parallelism'] = 4

print(properties)
