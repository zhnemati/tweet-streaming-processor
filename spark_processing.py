# pylint: disable= W0614, W0622, W0401, W0613
'''
This module fetches raw tweets from kafka, processes them and dumps them to psql sink
'''
from pathlib import Path
import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.functions import *
from pyspark.sql.types import *
from dotenv import load_dotenv
import pandas as pd


#Reading the provided csv file with data of drivers,teams and countries
df = pd.read_csv ('/home/zain/Downloads/data.csv')
#Loading the credentials from env
dotenv_path = Path('/home/zain/Documents/credentials.env')
DATA=load_dotenv(dotenv_path=dotenv_path)
KAFKA_TOPIC_NAME = os.getenv("KAFKA_TOPIC_NAME")
KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER")
CHECKPOINT_LOCATION = os.getenv("CHECKPOINT_LOCATION")
POSTGRES_USERNAME=os.getenv("POSTGRES_USERNAME")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
JDBC_CONNECTION_STRING=os.getenv("JDBC_CONNECTION_STRING")


if __name__ == "__main__":
    #Initiating spark session and providing external spark jar for jdbc sink
    spark = (
        SparkSession.builder.appName("Kafka Pyspark Streaming Learning")
        .master("local[*]")
        .config("spark.jars","/home/zain/Documents/postgresql-42.5.0.jar")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    #Read data stream from kafka
    sampleDataframe = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVER)
        .option("subscribe", KAFKA_TOPIC_NAME)
        .option("startingOffsets", "earliest")
        .option("failOnDataLoss","false")
        .load()
    )
    #Initializing and defining structure of dataframe to load the data into
    base_df = sampleDataframe.selectExpr("CAST(value as STRING)", "timestamp")
    SCHEMA = (
        StructType()
        .add("tweet", StringType())
    )
    info_dataframe = base_df.select(
        from_json(col("value"), SCHEMA).alias("sample"), "timestamp"
    )
    info_df_fin = info_dataframe.select("sample.*","timestamp")
    #Create an empty df to which the modified data will be appended for each micro batch
    df_temp=info_df_fin.select("*").withColumn("Driver_name",lit(""))\
    .withColumn("Team",lit("")).withColumn("Country",lit("")).limit(0)
    for i in df.itertuples():
        #For tweets containing driver name and team name add the name of
        #the driver and team to respective columns otherwise pass a standard string
        df_temp=df_temp.union(info_df_fin.select("*").distinct().\
        withColumn("Driver_name",f.when(f.col('tweet').rlike(i.Driver) &\
         f.col('tweet').rlike(i.Team) ,i.Driver)\
        .otherwise("Match not found")).\
        withColumn("Team",f.when(f.col('tweet').rlike(i.Team) & f.col('tweet').\
        rlike(i.Driver) ,i.Team).otherwise("Match not found")).\
        withColumn("Country",f.when(f.col('tweet').rlike(i.Driver) & \
        f.col('tweet').rlike(i.Team),i.Country).otherwise("Match not found")))
    df_final=df_temp.distinct()
    #Setting up jdbc sink with foreachbatch
    def _write_streaming(data_frame,epoch_id) -> None:
        data_frame.write \
            .mode('append') \
            .format("jdbc") \
            .option("url", JDBC_CONNECTION_STRING) \
            .option("dbtable", 'twitterdata.sparkdata') \
            .option("user", POSTGRES_USERNAME) \
            .option("password", POSTGRES_PASSWORD) \
            .save()
    #Write to postgres sink
    df_final.writeStream.foreachBatch(_write_streaming).start().awaitTermination()
