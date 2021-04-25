#!/usr/bin/env python
# -*-conding:utf-8-*-

import logging

from pyspark import SparkContext

logging.basicConfig(format='%(message)s', level=logging.INFO)

# import local file
test_file_name = "../README.md"
out_file_name = "file:///var/lib/hadoop-hdfs/spark_test/spark-out"

sc = SparkContext("local", "wordcount app")

# text_file rdd object
text_file = sc.textFile(test_file_name)

# counts
counts = text_file\
    .flatMap(lambda line: line.split(" "))\
    .map(lambda word: (word, 1))\
    .reduceByKey(lambda a, b: a + b)

# counts.saveAsTextFile(out_file_name)
output = counts.collect()

for (word, count) in output:
    print(word, count)
