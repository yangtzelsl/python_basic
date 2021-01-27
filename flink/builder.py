# -*- coding: utf-8 -*-
import json

KAFKA_SETTINGS = """
( 'properties.sasl.jaas.config' = 'org.apache.kafka.common.security.plain.PlainLoginModule  required  username="ptreader"password="pt30@123";' ,
'properties.bootstrap.servers' = '172.16.7.10:9092' ,
'connector' = 'kafka' ,
'properties.sasl.mechanism' = 'PLAIN' ,
'format' = 'json' ,
'properties.security.protocol' = 'SASL_PLAINTEXT' ,
'properties.group.id' = 'test' ,
'topic' = 'facebook' ,
'scan.startup.mode'='earliest-offset',
'json.ignore-parse-errors' = 'true'
)
"""


class Solution(object):
    def __init__(self):
        self.py_json_to_dsl = {
            # unicode是python2支持的语法, python3支持为str
            # unicode: "string",
            str: "string",
            int: "int",
            float: "decimal",
            bool: "boolean",
            None: "null",
            list: "array"
            # python3只有int,没有long
            # long: "long"
        }
        self.dsl_to_flink_sql = {
            "string": "string",
            "decimal": "DOUBLE",
            "int": "int",
            "boolean": "boolean",
            "null": "string",
            "datetime": "string",
            "long": "BIGINT",
            "array": "ARRAY"
        }
        self.dsl_to_hive_sql = {
            "string": "string",
            "decimal": "DOUBLE",
            "int": "int",
            "boolean": "boolean",
            "null": "string",
            "datetime": "string"
        }
        self.dsl = {}
        self.flink_sql = {}

    def source_to_dsl(self):
        """
        原始数据推测出测定值
        :return:
        """
        self.dsl = self.source_dfs(self.source)

    def dsl_to_flink(self):
        pass

    def dsl_to_hive(self):
        pass

    def source_dfs(self, source, dsl={}):
        for key in source:
            value = source[key]
            type_v = type(value)
            if type_v == str or type_v == int or type_v == float or type_v == list:
                dsl[key] = {"type": self.py_json_to_dsl[type_v]}
            elif type_v == dict:
                dsl[key] = self.source_dfs(source[key], {})
            # 如果key没有包含type字段，手动给定一个type(但可能存在问题)
            elif type_v == type(None):
                dsl[key] = {"optional": "true", "type": "string"}
            else:
                print("fuck !!!!!!!!!" + key)
        return dsl

    def flink_source_schema(self, dsl={}):
        sql = ""
        for key in dsl:
            if len(sql) != 0:
                sql += ", "
            if "type" in dsl[key]:
                if dsl[key]["type"] == "datetime":
                    if "format" in dsl[key]:
                        sql += "`" + key + "`" + "  " + "string"
                    else:
                        sql += "`" + key + "`" + "  " + "BIGINT"
                else:
                    sql += "`" + key + "`" + "  " + self.dsl_to_flink_sql[dsl[key]["type"]]
            # 对象类型，递归
            else:
                sql += "`" + key + "`" + " ROW<{0}>".format(self.flink_source_schema(dsl[key]))
        return sql

    def hive_sink_schema(self, dsl, prefix="", sql=""):
        for key in dsl:
            if len(sql) != 0:
                sql += ", "
            if "type" in dsl[key]:
                if dsl[key]["type"] == "datetime":
                    sql += "`" + prefix + key + "`" + "  " + 'TIMESTAMP'
                else:
                    sql += "`" + prefix + key + "`" + "  " + self.dsl_to_hive_sql[dsl[key]["type"]]
            else:
                sql = self.hive_sink_schema(dsl[key], prefix + key + "_", sql)
        return sql

    def flat_sql(self, dsl, prefix="", sql=""):
        for key in dsl:
            if len(sql) != 0:
                sql += ", "
            if "type" in dsl[key]:
                if dsl[key]["type"] == "datetime":
                    if "format" in dsl[key]:
                        sql += "TO_TIMESTAMP({0}, '{1}') ".format(prefix + key, dsl[key]["format"])
                    else:
                        sql += "TO_TIMESTAMP(FROM_UNIXTIME({0}, 'yyyy-MM-dd HH:mm:ss'))".format(prefix + key) + " "
                else:
                    sql += "" + prefix + key + "" + "  "
            else:
                sql = self.flat_sql(dsl[key], prefix + key + ".", sql[:-2])
        return sql

    def process(self, source):
        result = {}

        flink_create_sql = " {schema} "

        hive_create_sql = """
        create table {ta} ({schema}) 
        PARTITIONED BY (gt int) STORED AS PARQUET 
        TBLPROPERTIES ('sink.partition-commit.trigger' = 'process-time',
        'sink.partition-commit.delay' = '1 min',
        'sink.partition-commit.policy.kind' = 'metastore,success-file',
        'is_generic'='false')
        """

        flink_insert_sql = "INSERT INTO {sink} select {para} from source_{ta} where table_type='{type}' "

        result = flink_create_sql.format(schema=self.flink_source_schema(source))

        # for table in source:
        #     # 每次遍历会先清空
        #     result.setdefault(table, {})
        #     print(table)
        #
        #     result['source'] = flink_create_sql.format(schema=self.flink_source_schema(source))
        #
        #     # result[table]["sink"] = hive_create_sql.format(
        #     #     ta=table,
        #     #     schema=self.hive_sink_schema(source[table]["check_rule"])
        #     # )
        #     #
        #     # result[table]["process"] = flink_insert_sql.format(
        #     #     sink=table,
        #     #     ta=table,
        #     #     para=self.flat_sql(
        #     #         source[table]["check_rule"]) + ", cast(DATE_FORMAT(data.gather_time,'yyyyMMdd') as int)",
        #     #     type=table.split("_")[-1]
        #     # ) + " "

        return result


if __name__ == "__main__":
    # str3 = '{"vendor": "tg", "push_time": 1609205855, "platform": "facebook", "uuid": "2b6018bc73c33c5e8635b316cb8ea657", "table_type": "post", "data": {"timeline_like_count": 0, "timeline_longitude": null, "love_count": 0, "timeline_comment_count": 0, "timeline_create_time": "2020-12-29 09:16:44", "timeline_is_original": 0, "author_name": "Eddie Mak", "timeline_content": "", "timeline_loaction": null, "file_info": "", "author_id": "1045483254", "gather_time": "2020-12-29 09:37:34", "timeline_share_title": "\u4eab\u53d7\u7535\u5f71 was live.", "hug_count": 0, "haha_count": 0, "sad_count": 0, "wow_count": 0, "timeline_latitude": null, "timeline_url": "https://www.facebook.com/story.php?story_fbid=10222560832223281&id=1045483254", "timeline_share_content": "\u4e00\u65e9\u8a71\u4f50 \u505a\u53e4\u60d1\u4ed4\u9072\u65e9\u6a6b\u5c38\u8857\u982d \u9023\u8001\u5a46\u90fd\u6703\u88ab\u4eba\u641e", "timeline_title": "Eddie Mak", "collect_company": "TG", "timeline_feedback_id": "1045483254_10222560832223281", "timeline_id": "10222560832223281", "angry_count": 0, "update_time": "2020-12-29 09:16:44", "timeline_share_count": 0}}'
    str2 = '{"id":7106,"name":"KuxQVF1a","date1":"2021-02-06","obj1":{"time1":"14:26:50","str1":"sfasfafs","long1":2324342345},"arr1":[{"f1":"f1str11","f2":8},{"f1":"f1str22","f2":5}],"time1":"14:26:50","timestamp1":"2021-01-19 14:26:50","map1":{"flink":830},"mapinmap":{"inner_map":{"key1":7}}}'
    str4 = '{"id":3537,"name":"Lz2yM03A","date1":"2021-02-17","obj1":{"time1":"17:50:19","str1":"sfasfafs","long1":2324342345},"time1":"17:50:19","timestamp1":"2021-01-19 17:50:19","map1":{"flink":842}}'
    s = Solution().source_dfs(json.loads(str4), {})

    json_s = json.dumps(s)
    # print(json_s)
    # print(json.loads(json_s))

    str1 = """
    {"data":{"forward_group_id":{"empty":true,"max_len":32,"optional":true,"type":"string"},"forward_user_id":{"empty":true,"max_len":32,"optional":true,"type":"string"}},"platform":{"enumerate":["telegram"],"type":"string"},"push_time":{"gte":["data","gather_time"],"type":"datetime"},"table_type":{"enumerate":["comment"],"type":"string"},"uuid":{"len":32,"type":"string"},"vendor":{"enumerate":["ws"],"type":"string"}}
    """
    # print(json.loads(str1))
    # print(type(json.loads(str1)))

    test_str = """
    {"id": {"type": "int"}, "obj1": {"str1": {"type": "string"}, "str2": {"type": "string"}}, "timestamp1": {"type": "datetime"}}
    """

    process = Solution().process(json.loads(json_s))
    print(json.dumps(process))
