#!/bin/bash
pylint spark_processing.py
wget https://downloads.apache.org/spark/spark-3.3.0/spark-3.3.0-bin-hadoop3.tgz
tar xvf spark-*
sudo mv spark-3.3.0-bin-hadoop3 /opt/spark
echo "export SPARK_HOME=/opt/spark" >> ~/.profile
echo "export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin" >> ~/.profile
echo "export PYSPARK_PYTHON=/usr/bin/python3" >> ~/.profile
start-master.sh
start-slave.sh spark://RF-ZAIN-N:7077
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 --driver-class-path postgresql-42.5.0.jar spark-processing.py 
psql -U postgres -h localhost -d postgres -p 5432 -f - <<EOF
\i fetch_from_psql.sql;
EOF