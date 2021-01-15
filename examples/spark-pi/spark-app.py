import sys
import os
from random import random
from operator import add

from pyspark import SparkConf
from pyspark.sql import SparkSession

# Instantiate a spark configuration object to receive settings
spark_conf = SparkConf()

# Configure some basic spark cluster sizing parameters
spark_conf.set('spark.executor.cores', '1')
spark_conf.set('spark.executor.instances', '2')
spark_conf.set('spark.executor.memory', '900m')

# The name of your Spark cluster hostname or ip address
spark_cluster = os.environ['SPARK_CLUSTER']

print('Attaching to Spark cluster {cluster}'.format(cluster=spark_cluster)) 
spark = SparkSession.builder \
    .master('spark://{cluster}:7077'.format(cluster=spark_cluster)) \
    .appName('Spark-App-S2I-Demo') \
    .config(conf = spark_conf) \
    .getOrCreate()

partitions = 2
n = 100000 * partitions

def f(_):
    x = random() * 2 - 1
    y = random() * 2 - 1
    return 1 if x ** 2 + y ** 2 <= 1 else 0

print('Running Spark job to compute pi')
count = spark.sparkContext.parallelize(range(1, n + 1), partitions).map(f).reduce(add)

print('====================================================')
print("Pi is roughly %f" % (4.0 * count / n))
print('====================================================')

spark.stop()
