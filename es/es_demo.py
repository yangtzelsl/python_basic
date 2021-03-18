# -.- coding:utf-8 -.-
import json
from elasticsearch import Elasticsearch

# 快速取出ES索引中该索引所有字段名称
# 1、通过命令 GET  索引名称/_mapping 获取该索引所有字段信息
# 2、取出"properties"中所有字段，如test_dict中
# 3、通过test_dict.keys()获取所有字段值
# 4、转化为list, list(test_dict.keys()),输出结果可以直接用于获取数据的所有字段

es = Elasticsearch("10.36.5.120")
index_name = "fault_log"

# 查询方式1：通过所有数据查询
res = es.search(index=index_name, body={"query": {"match_all": {}}})
# print(type(res))
# print(res)
keys = res.get("hits").get("hits")
print(keys)
print(keys[0])
print(keys[0].get("_source").keys())
# for key in keys:
#     print(key)

# 查询方式2：通过索引+属性查询
res2 = es.get(index=index_name, doc_type="_mapping", id="*")
print(res2)
res3 = res2.get(index_name).get("mappings").get("_doc").get("properties")
print(type(res3))
print(res3.keys())
# print(res2.get(index_name).get("mappings").get("_doc").get("properties").keys())

print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

log_info = json.dumps(res3, ensure_ascii=False, sort_keys=False, indent=4, separators=(',', ': '))
# print(log_info)
# print(list(log_info.keys()))
# print(res.keys())

test_dict = {
    "field0": {
        "type": "keyword"
    },
    "@timestamp": {
        "type": "date"
    },
    "field1": {
        "type": "keyword"
    },
    "field2": {
        "type": "keyword"
    }
}
# print(list(test_dict.keys()))
