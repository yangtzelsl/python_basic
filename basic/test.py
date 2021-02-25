import json

dict1 = {'create_by': '',
         'update_by': '',
         'description': 'flink_type',
         'id': 134457,
         'name': 'flink_type',
         'alias': 'flink_type',
         'type': 'source',
         'database': '',
         'mapping': {'id': ['id'], 'inner': ['obj1', 'str1', 'inner'], 'str2': ['obj1', 'str2']},
         'storage_cluster': 30001,
         'fields': [{'field_name': 'id', 'alias': 'id', 'field_type': 'bigint', 'is_dimension': 0},
                    {'field_name': 'inner', 'alias': 'str1', 'field_type': 'string', 'is_dimension': 0},
                    {'field_name': 'str2', 'alias': 'str2', 'field_type': 'string', 'is_dimension': 0}
                    ]
         }
# 当前如果内层和外层出现同名的key值，虽然路径不同，但这种映射方式会出现问题
# 实际解析会有bug，被吞掉一层
# {'id': ['id'], 'inner': ['obj1', 'str1', 'inner'], 'inner': ['obj1', 'inner']}
# mds("@".join(['obj1', 'str1', 'inner']))

dict2 = {
    "obj1": {"str1": {"type": "string"}, "str2": {"type": "string"}},
    "id": {"type": "bigint"}
}


def test():
    b_dict = {}
    for key in dict1.keys():
        # print(key)
        # print(key, dict1.get(key))
        new_dict = {}
        if key == "mapping":
            dict_value = dict1.get(key)
            for tmp in dict_value:
                new_dict = {tmp: dict_value.get(tmp)}
                # print(tmp, dict_value.get(tmp))
                # for obj in dict_value.get(tmp):
                #     print(obj)

        if key == "fields":
            dict_fields = dict1.get("fields")
            # 遍历字段
            for fields in dict_fields:
                dict_mapping = dict1.get('mapping')
                # 遍历映射
                for mapping_key in dict_mapping:
                    inner_list = []
                    if fields.get('field_name') == mapping_key:
                        # print(fields.get('field_type'), dict_mapping.get(mapping_key))
                        list_mapping = dict_mapping.get(mapping_key)
                        if len(list_mapping) == 1:
                            b_dict = {list_mapping[0]: {"type": fields.get('field_type')}}
                        elif len(list_mapping) > 1:
                            inner_list.append({list_mapping[1]: {"type": fields.get('field_type')}})
                            b_dict = {list_mapping[0]: inner_list}


b_dict = {}
inner_list = []
dict_fields = dict1.get("fields")
# 遍历字段
for fields in dict_fields:
    dict_mapping = dict1.get('mapping')
    # 遍历映射
    for mapping_key in dict_mapping:
        if fields.get('field_name') == mapping_key:
            # print(fields.get('field_type'), dict_mapping.get(mapping_key))
            list_mapping = dict_mapping.get(mapping_key)
            if len(list_mapping) < 1:
                print("有错误!!!")
                pass
            elif len(list_mapping) == 1:
                b_dict[list_mapping[0]] = {"type": fields.get('field_type')}
            else:
                # inner_list.append({list_mapping[1]: {"type": fields.get('field_type')}})
                b_dict.setdefault("type", fields.get('field_type'))
                # b_dict[list_mapping[0]] = inner_list
# print(b_dict)


def route_to_json1():
    js = dict()
    for each in dict1["mapping"]:
        step = js
        val_key = dict2
        for road in dict1["mapping"][each]:
            # 路径已有
            val_key = val_key[road]
            if road in step:
                pass
            # 路径没有
            else:
                step.setdefault(road, {})
            step = step[road]
        step.setdefault("type", val_key["type"])
    print(json.dumps(js))
    print("json build ok")


def route_to_json():
    js = dict()
    # prepare
    type_dic = dict()
    for each in dict1["fields"]:
        type_dic.setdefault(each["field_name"], each["field_type"])

    for each in dict1["mapping"]:
        step = js
        last_road = None
        for road in dict1["mapping"][each]:
            # 路径已有
            if road in step:
                pass
            # 路径没有
            else:
                step.setdefault(road, {})
            step = step[road]
            last_road = road

        step.setdefault("type", type_dic.get(last_road))
    return json.dumps(js)


if __name__ == "__main__":
    # result = route_to_json1()
    # print(result)
    teststr = """
    {"vendor":"black_market_spider","push_time":1613707211,"full_eid":"","spec_eid ":"ab0d3ba52adc4252a4c3aad369d2575486459ca6","type":"spec","index_type":"goods","data":{"crawl_time":"2021-02-19T04:00:11","domain":"5xxqhn7qbtug7cag.onion","net_type":"tor","spider_name":"black_market_spider","goods_name":"Heckler & Koch MP5 A5 .22LR","goods_id":"Heckler & Koch MP5 A5 .22LR","url":"http://5xxqhn7qbtug7cag.onion/","goods_info":"Caliber: .22LR\r\n\r\nCapacity: Two 25 round magazines included\r\n\r\nBarrel: 16.1\", 1:13.75\" Twist\r\n\r\nLength: 26.8\" - 33.8\"\r\n\r\nWeight: ~6 pounds","goods_img_url":["http://5xxqhn7qbtug7cag.onion/more/hkmp5.jpg"],"crawl_category":"数据","crawl_category_1":["数据"],"goods_type":["数据"],"goods_tag":["数据"],"goods_buyer":["1美元  2020   12000","2美元  2020   12000"],"sold_count":112,"price":["$400"],"user_id":"BMG","user_name":"BMG","goods_area":"USA","goods_ship_to":["USA"],"publish_time":"2021-02-19T04:00:11","raw_publish_time":"2021年2月19日","goods_update_time":"2021-02-19T04:00:11","goods_browse_count":1,"goods_feedback_count":1,"goods_acquisition_count":1,"goods_accepted_crypto_currency":["BTC","ETH"],"goods_payment_method":"onion","sku_quantify":100,"price_quantify":400,"sku":"100件","bitcoin_addresses":[],"eth_addresses":[],"is_extracted":false,"is_relation_extracted":false,"is_analyzed":false,"gmt_create":"2021-02-19T04:00:11","gmt_modified":"2021-02-19T04:00:11"}}
    """
    # （1）""""""三引号里面的内容是python str（不是json），dumps先转成json,
    # （2）loads再将json转成需要的python 对象
    print(json.loads(json.dumps(teststr)))
