#!/bin/bash
pylint tweet_reader.py
sudo apt update  
sudo apt install default-jdk 
wget https://dlcdn.apache.org/kafka/3.2.0/kafka_2.12-3.3.1.tgz
tar xzf kafka_2.12-3.3.1.tgz 
sudo mv kafka_2.12-3.3.1 /usr/local/kafka  
sudo systemctl start zookeeper 
sudo systemctl start kafka
/usr/local/kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic twitter-data
python3 tweet-reader.py