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


class Soluation(object):
    def __init__(self):
        self.py_json_to_dsl = {
            # unicode是python2支持的语法, python3支持为str
            # unicode: "string",
            str: "string",
            int: "int",
            float: "decimal",
            bool: "boolean",
            None: "null",
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
            "long": "BIGINT"
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
            elif type_v == type(None):
                dsl[key] = {"optional": "true"}
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

        flink_create_sql = "CREATE TABLE  source_{ta} ({schema}) with " + KAFKA_SETTINGS

        hive_create_sql = """
        create table {ta} ({schema}) 
        PARTITIONED BY (gt int) STORED AS PARQUET 
        TBLPROPERTIES ('sink.partition-commit.trigger' = 'process-time',
        'sink.partition-commit.delay' = '1 min',
        'sink.partition-commit.policy.kind' = 'metastore,success-file',
        'is_generic'='false')
        """

        flink_insert_sql = "INSERT INTO {sink} select {field}, count(*) from source_{ta} where table_type='{type}' group by '{field}' "

        for table in source:
            # 每次遍历会先清空
            result.setdefault(table, {})

            result[table]["source"] = flink_create_sql.format(
                schema=self.flink_source_schema(source[table]["check_rule"]),
                ta=table)

            result[table]["sink"] = hive_create_sql.format(
                ta=table,
                schema=self.hive_sink_schema(source[table]["check_rule"])
            )

            result[table]["process"] = flink_insert_sql.format(
                sink=table,
                ta=table,
                field=self.flat_sql(
                    source[table]["check_rule"]) + ", cast(DATE_FORMAT(data.gather_time,'yyyyMMdd') as int)",
                type=table.split("_")[-1]
            ) + " "

        return result


if __name__ == "__main__":
    stri = '{"vendor": "tg", "push_time": 1609205855, "platform": "facebook", "uuid": "2b6018bc73c33c5e8635b316cb8ea657", "table_type": "post", "data": {"timeline_like_count": 0, "timeline_longitude": null, "love_count": 0, "timeline_comment_count": 0, "timeline_create_time": "2020-12-29 09:16:44", "timeline_is_original": 0, "author_name": "Eddie Mak", "timeline_content": "", "timeline_loaction": null, "file_info": "", "author_id": "1045483254", "gather_time": "2020-12-29 09:37:34", "timeline_share_title": "\u4eab\u53d7\u7535\u5f71 was live.", "hug_count": 0, "haha_count": 0, "sad_count": 0, "wow_count": 0, "timeline_latitude": null, "timeline_url": "https://www.facebook.com/story.php?story_fbid=10222560832223281&id=1045483254", "timeline_share_content": "\u4e00\u65e9\u8a71\u4f50 \u505a\u53e4\u60d1\u4ed4\u9072\u65e9\u6a6b\u5c38\u8857\u982d \u9023\u8001\u5a46\u90fd\u6703\u88ab\u4eba\u641e", "timeline_title": "Eddie Mak", "collect_company": "TG", "timeline_feedback_id": "1045483254_10222560832223281", "timeline_id": "10222560832223281", "angry_count": 0, "update_time": "2020-12-29 09:16:44", "timeline_share_count": 0}}'
    s = Soluation().source_dfs(json.loads(stri), {})
    print(json.dumps(s))

    #     str = """
    # {"telegram_comment":{"check_rule":{"data":{"collect_company":{"enumerate":["WS"],"type":"string"},"file_info":{"empty":true,"optional":true,"reg":{"para":"a","relation":"full_match"},"type":"string"},"file_type":{"empty":true,"enumerate":["1","2","3"],"optional":true,"type":"string"},"forward_group_id":{"empty":true,"max_len":32,"optional":true,"type":"string"},"forward_user_id":{"empty":true,"max_len":32,"optional":true,"type":"string"},"gather_time":{"format":"yyyy-MM-dd HH:mm:ss","gte":["data","msg_time"],"type":"datetime"},"is_repeat":{"enumerate":["是","否"],"type":"string"},"last_edit_time":{"empty":true,"format":"yyyy-MM-dd HH:mm:ss","gte":["data","msg_time"],"optional":true,"type":"datetime"},"msg_time":{"format":"yyyy-MM-dd HH:mm:ss","type":"datetime"},"read_count":{"min":0,"type":"int"},"received_tg_id":{"empty":true,"max_len":32,"optional":true,"type":"string"},"reply_tg_id":{"min":0,"type":"int"},"reply_tg_msg":{"empty":true,"optional":true,"type":"string"},"sender_tg_id":{"empty":true,"max_len":32,"optional":true,"type":"string"},"tg_gro_id":{"max_len":32,"type":"string"},"tg_msg":{"empty":true,"optional":true,"type":"string"},"tg_msg_id":{"min":0,"type":"int"},"tg_msg_type":{"empty":true,"max_len":32,"optional":true,"type":"string"}},"platform":{"enumerate":["telegram"],"type":"string"},"push_time":{"gte":["data","gather_time"],"type":"datetime"},"table_type":{"enumerate":["comment"],"type":"string"},"uuid":{"len":32,"type":"string"},"vendor":{"enumerate":["ws"],"type":"string"}}},"telegram_group":{"check_rule":{"data":{"collect_company":{"enumerate":["PT","WS"],"type":"string"},"create_time":{"format":"yyyy-MM-dd HH:mm:ss","type":"datetime"},"gather_time":{"format":"yyyy-MM-dd HH:mm:ss","gt":["data","create_time"],"type":"datetime"},"group_info":{"empty":true,"max_len":500,"optional":true,"type":"string"},"member_count":{"min":0,"type":"int"},"tg_gc_type":{"enumerate":["channel","group"],"type":"string"},"tg_gro_acc":{"empty":true,"max_len":32,"optional":true,"type":"string"},"tg_gro_head_img":{"empty":true,"optional":true,"reg":{"para":"a","relation":"full_match"},"type":"string"},"tg_gro_id":{"empty":true,"max_len":32,"optional":true,"type":"string"},"tg_gro_name":{"max_len":150,"type":"string"},"tg_gro_url":{"empty":true,"optional":true,"reg":{"para":"a","relation":"full_match"},"type":"string"},"tg_menb_count":{"min":0,"type":"int"}},"platform":{"enumerate":["telegram"],"type":"string"},"push_time":{"gte":["data","gather_time"],"type":"datetime"},"table_type":{"enumerate":["group"],"type":"string"},"uuid":{"len":32,"type":"string"},"vendor":{"enumerate":["ws","pt"],"type":"string"}}},"telegram_message":{"check_rule":{"data":{"collect_company":{"enumerate":["PT"],"type":"string"},"file_info":{"empty":true,"optional":true,"reg":{"para":"a","relation":"full_match"},"type":"string"},"file_type":{"empty":true,"enumerate":["1","2","3"],"optional":true,"type":"string"},"forward_group_id":{"empty":true,"max_len":32,"optional":true,"type":"string"},"forward_user_id":{"empty":true,"max_len":32,"optional":true,"type":"string"},"gather_time":{"format":"yyyy-MM-dd HH:mm:ss","gte":["data","msg_time"],"type":"datetime"},"is_repeat":{"enumerate":["是","否"],"type":"string"},"last_edit_time":{"empty":true,"format":"yyyy-MM-dd HH:mm:ss","gte":["data","msg_time"],"optional":true,"type":"datetime"},"msg_time":{"format":"yyyy-MM-dd HH:mm:ss","type":"datetime"},"read_count":{"min":0,"type":"int"},"received_tg_id":{"empty":true,"max_len":32,"optional":true,"type":"string"},"reply_tg_id":{"min":0,"type":"int"},"reply_tg_msg":{"empty":true,"optional":true,"type":"string"},"sender_tg_id":{"empty":true,"max_len":32,"optional":true,"type":"string"},"tg_gro_id":{"max_len":32,"type":"string"},"tg_msg":{"empty":true,"optional":true,"type":"string"},"tg_msg_id":{"min":0,"type":"int"},"tg_msg_type":{"empty":true,"max_len":32,"optional":true,"type":"string"}},"platform":{"enumerate":["telegram"],"type":"string"},"push_time":{"gte":["data","gather_time"],"type":"datetime"},"table_type":{"enumerate":["message"],"type":"string"},"uuid":{"len":32,"type":"string"},"vendor":{"enumerate":["pt"],"type":"string"}}},"telegram_user":{"check_rule":{"data":{"collect_company":{"enumerate":["PT","WS"],"type":"string"},"gather_time":{"format":"yyyy-MM-dd HH:mm:ss","type":"datetime"},"head_img":{"empty":true,"optional":true,"reg":{"para":"a","relation":"full_match"},"type":"string"},"tel":{"empty":true,"max_len":32,"optional":true,"type":"string"},"tg_acc":{"empty":true,"max_len":50,"optional":true,"type":"string"},"tg_id":{"max_len":32,"type":"string"},"tg_nick_name":{"empty":true,"max_len":50,"optional":true,"type":"string"},"user_background":{"empty":true,"max_len":50,"optional":true,"type":"string"},"user_status":{"empty":true,"max_len":32,"optional":true,"type":"string"}},"platform":{"enumerate":["telegram"],"type":"string"},"push_time":{"gte":["data","gather_time"],"type":"datetime"},"table_type":{"enumerate":["user"],"type":"string"},"uuid":{"len":32,"type":"string"},"vendor":{"enumerate":["pt","ws"],"type":"string"}}},"telegram_user_group":{"check_rule":{"data":{"collect_company":{"enumerate":["PT","WS"],"type":"string"},"gather_time":{"format":"yyyy-MM-dd HH:mm:ss","type":"datetime"},"tg_gro_id":{"empty":true,"max_len":32,"optional":true,"type":"string"},"tg_gro_ro":{"empty":true,"max_len":50,"optional":true,"type":"string"},"tg_id":{"max_len":32,"type":"string"},"user_join_time":{"empty":true,"format":"yyyy-MM-dd HH:mm:ss","optional":true,"type":"datetime"}},"platform":{"enumerate":["telegram"],"type":"string"},"push_time":{"gte":["data","gather_time"],"type":"datetime"},"table_type":{"enumerate":["user_group"],"type":"string"},"uuid":{"len":32,"type":"string"},"vendor":{"enumerate":["pt","ws"],"type":"string"}}}}
    #     """
    str1 = """
    {"telegram_comment":{"check_rule":{"data":{"forward_group_id":{"empty":true,"max_len":32,"optional":true,"type":"string"},"forward_user_id":{"empty":true,"max_len":32,"optional":true,"type":"string"}},"platform":{"enumerate":["telegram"],"type":"string"},"push_time":{"gte":["data","gather_time"],"type":"datetime"},"table_type":{"enumerate":["comment"],"type":"string"},"uuid":{"len":32,"type":"string"},"vendor":{"enumerate":["ws"],"type":"string"}}}}
    """

    str2 = """
    {"a":{"check_rule":{"id": {"type": "int"}, "obj1": {"str1": {"type": "string"}, "str2": {"type": "string"}}, "timestamp1": {"type": "datetime"}}}}
    """
    print(json.dumps(Soluation().process(json.loads(str2))))
