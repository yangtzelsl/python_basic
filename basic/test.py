dict1 = {'create_by': '',
         'update_by': '',
         'description': 'flink_type',
         'id': 134457,
         'name': 'flink_type',
         'alias': 'flink_type',
         'type': 'source',
         'database': '',
         'mapping': {'id': ['id'], 'str1': ['obj1', 'str1'], 'str2': ['obj1', 'str2']},
         'storage_cluster': 30001,
         'fields': [{'field_name': 'id', 'alias': 'id', 'field_type': 'bigint', 'is_dimension': 0},
                    {'field_name': 'str1', 'alias': 'str1', 'field_type': 'string', 'is_dimension': 0},
                    {'field_name': 'str2', 'alias': 'str2', 'field_type': 'string', 'is_dimension': 0}
                    ]
         }

dict2 = {
    "obj1": {"str1": {"type": "string"}, "str2": {"type": "string"}},
    "id": {"type": "bigint"}
}

for key in dict1.keys():
    # print(key)
    # print(key, dict1.get(key))
    if key == "mapping":
        dict_value = dict1.get(key)
        for tmp in dict_value:
            print(tmp, dict_value.get(tmp))
            for obj in dict_value.get(tmp):
                print(obj)

    if key == "fields":
        dict_value = dict1.get(key)
        for tmp in dict_value:
            print(tmp)