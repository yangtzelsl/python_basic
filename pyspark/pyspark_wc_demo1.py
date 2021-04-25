# 注意这两行代码要放最上面，放其它地方不行
import findspark

findspark.init()
import sys
from operator import add

# SparkSession：是一个对Spark的编程入口，取代了原本的SQLContext与HiveContext，方便调用Dataset和DataFrame API
# SparkSession可用于创建DataFrame，将DataFrame注册为表，在表上执行SQL，缓存表和读取parquet文件。
from pyspark.sql import SparkSession

if __name__ == "__main__":

    # Python 常用的简单参数传入
    if len(sys.argv) != 2:
        print("Usage: wordcount <file>", file=sys.stderr)
        exit(-1)

    # appName 为 Spark 应用设定一个应用名，改名会显示在 Spark Web UI 上
    # 假如SparkSession 已经存在就取得已存在的SparkSession，否则创建一个新的。
    spark = SparkSession \
        .builder \
        .appName("PythonWordCount") \
        .getOrCreate()

    # 读取传入的文件内容，并写入一个新的RDD实例lines中，此条语句所做工作有些多，不适合初学者，可以截成两条语句以便理解。
    # map是一种转换函数，将原来RDD的每个数据项通过map中的用户自定义函数f映射转变为一个新的元素。原始RDD中的数据项与新RDD中的数据项是一一对应的关系。
    lines = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])

    # flatMap与map类似，但每个元素输入项都可以被映射到0个或多个的输出项，最终将结果”扁平化“后输出
    counts = lines.flatMap(lambda x: x.split(' ')) \
        .map(lambda x: (x, 1)) \
        .reduceByKey(add) \
    # .reduceByKey((lambda a, b: a + b))

    # collect() 在驱动程序中将数据集的所有元素作为数组返回。 这在返回足够小的数据子集的过滤器或其他操作之后通常是有用的。由于collect 是将整个RDD汇聚到一台机子上，所以通常需要预估返回数据集的大小以免溢出。
    output = counts.collect()

    for (word, count) in output:
        print("%s: %i" % (word, count))

    spark.stop()
