# Tweet-streaming-processor
This is a streaming processor for live tweets, it fetches tweets based on a user-defined filter, writes them to a kafka topic from where the data is fed to spark stream processing engine which processes the data and sinks to a postgres DB.
(It is already assumed that you have kafka,psql and spark set up, either locally or on a remote machine on which you will be executing this code)
## Steps :
- Create a developer account on twitter with elevated access
- Once done acquire auth tokens, secret and access keys
- Set up and install python (If not done)
- Install the python libraries mentioned in the requirements.txt file
- Start the tweet_reader.py program
- Submit the spark job using the following command
```spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 --driver-class-path postgresql-42.5.0.jar spark_processing.py```
- Go to the psql client to query and verify the data in real time

