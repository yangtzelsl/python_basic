# -.- coding:utf-8 -.-
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class ElasticObj:
    def __init__(self, index_name, index_type, index_conf, ip="127.0.0.1"):
        """
        ElasticObj initialize
        :param index_name: 索引名称
        :param index_type: 索引类型
        """
        self.index_name = index_name
        self.index_type = index_type
        self.index_conf = index_conf
        # 无用户名密码状态
        self.es = Elasticsearch(hosts=[ip])
        # 用户名密码状态
        # self.es = Elasticsearch([ip], http_auth=('elastic', 'password'), port=9200)

    def create_index(self):
        """
        Create an index in ElasticSearch.
        :return:
        """
        if self.es.indices.exists(index=self.index_name) is not True:
            res = self.es.indices.create(index=self.index_name, body=self.index_conf)
            print("index created success: ", res)

    def bulk_index_data(self, in_data):
        """
        用bulk将批量数据存储到es
        :return:
        """
        actions = []
        for line in in_data:
            action = {
                "_index": self.index_name,
                "_type": self.index_type,
                "_id": line['id'],  # _id 也可以默认生成，不赋值
                "_source": line['data']
            }
            actions.append(action)
            # 批量处理
        success, _ = bulk(self.es, actions, index=self.index_name, raise_on_error=True)
        print('Performed %d actions' % success)

    def delete_index_data(self, in_id):
        """
        删除索引中的一条
        :param in_id:
        :return:
        """
        res = self.es.delete(index=self.index_name, doc_type=self.index_type, id=in_id)
        print("delete data from: ", res)

    def get_data_id(self, in_id):
        """
        通过 id查询
        :param in_id:
        :return:
        """
        res = self.es.get(index=self.index_name, doc_type=self.index_type, id=in_id)
        print(res['_source'])

        print('------------------------------------------------------------------')
        #
        # # 输出查询到的结果
        for hit in res['hits']['hits']:
            # print hit['_source']
            print(hit['_source']['date'], hit['_source']['source'], hit['_source']['link'], hit['_source']['keyword'], \
                hit['_source']['title'])

    def get_data_by_body(self):
        """
        通过 body查询
        :return:
        """
        # doc = {'query': {'match_all': {}}}
        doc = {
            "query": {
                "match": {
                    "keyword": "电视"
                }
            }
        }
        _searched = self.es.search(index=self.index_name, doc_type=self.index_type, body=doc)

        for hit in _searched['hits']['hits']:
            # print hit['_source']
            print(hit['_source']['date'], hit['_source']['source'], hit['_source']['link'], hit['_source']['keyword'], \
                hit['_source']['title'])

    def get_data_by_all(self):
        """
        查询该索引中所有数据
        :return:
        """
        res = self.es.search(index=self.index_name, body={"query": {"match_all": {}}})
        log_info = json.dumps(res, ensure_ascii=False, sort_keys=False, indent=4, separators=(',', ': '))
        print(log_info)


COUNTS = "counts"
T50 = "T50ms"
T70 = "T70ms"
T99 = "T99ms"
T100 = "T100ms"

def adproxy_es_operate():
    es_host = "172.16.7.52"
    es_index = "adproxy_log"
    es_index_type = "adproxy_log_type"
    es_index_conf = {
        'settings': {
            # just one shard, no replicas for testing
            'number_of_shards': 1,
            'number_of_replicas': 0,
        },
        "mappings": {
            es_index_type: {
                "properties": {
                    "desc": {
                        "type": "text"
                    },
                    "data_time": {
                        "type": "date",
                        "format": "yyyy-MM-dd HH:mm:ss,SSS"
                    },
                    COUNTS: {
                        "type": "integer"
                    },
                    T50: {
                        "type": "integer"
                    },
                    T70: {
                        "type": "integer"
                    },
                    T99: {
                        "type": "integer"
                    },
                    T100: {
                        "type": "integer"
                    }
                }
            }

        }
    }
    es_obj = ElasticObj(es_index, es_index_type, es_index_conf, ip=es_host)
    es_obj.create_index()
    data_info = [
        {
            "id": 1234567,
            "data": {
                "desc": "TBAD5",
                "data_time": "2019-05-08 12:30:00,000",
                COUNTS: 24756,
                T50: 14175,
                T70: 5305,
                T99: 2523,
                T100: 2753
            }
        },
        {
            "id": 12345678,
            "data": {
                "desc": "TBAD5",
                "data_time": "2019-05-07 12:35:00,000",
                COUNTS: 24533,
                T50: 14339,
                T70: 5379,
                T99: 2513,
                T100: 14339
            }
        },
        {
            "id": 123456789,
            "data": {
                "desc": "TBAD5",
                "data_time": "2019-05-08 12:35:00,000",
                COUNTS: 24533,
                T50: 14339,
                T70: 5379,
                T99: 2513,
                T100: 14339
            }
        },
        {
            "id": 1234567890,
            "data": {
                "desc": "TBAD5",
                "data_time": "2019-05-09 12:35:00,000",
                COUNTS: 24533,
                T50: 14339,
                T70: 5379,
                T99: 2513,
                T100: 14339
            }
        },
    ]
    es_obj.bulk_index_data(data_info)
    es_obj.get_data_by_all()


if __name__ == '__main__':
    adproxy_es_operate()