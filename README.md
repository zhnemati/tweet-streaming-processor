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

## Assumptions:
Original sample data provided data with teams and drivers were modified in following way to extract maximum amount of data :  
Team names were modified in the following pattern : 
Mercedes AMG Petronas F1 Team - > Mercedes
Red Bull Racing -> Red Bull
Scuderia Ferrari Formula 1 -> Ferrari
McLaren Racing -> McLaren 
Etc. 

For Drivers:
Lewis Hamilton -> Hamilton
George Russell -> Russell
Max Verstappen -> Verstappen
Etc.

This was done to capture the maximum amount of tweets using regex matching as most tweets do not have the team's complete name, i.e. Mercedes AMG Petronas F1 Team or Sergio “Checo” Perez in case of drivers. With this modification, the goal was to extract the maximum amount of data. In case any tweet did contain complete names that would not be affected by this approach as sir name of the driver or the primary name of the team would still be contained within the string
Incase the data is strictly needed to be evaluated against the provided dataset, that can be done as well
The streaming processor was run for a duration of 3-4 hours
To run the code, make sure kafka,spark and python are set up locally
The bash script also does the same job but it may run into issues depending on the system specs and host os
Approach:
The data is fetched from Twitter streaming API with filters ‘Formula 1, F1, Forumla1’  and fed to a Kafka topic, the Kafka server is set up locally
Spark is set up locally and using pyspark the data is ingested from the Kafka topic
The raw data has tweets and timestamp
The tweet undergoes a regex matching process to find the names of drivers and teams if they have been mentioned in the string
If they are found the names are appended to the driver_name and team column of the same data frame and if not found a sample placeholder string is appended. 
The data is written to a psql client set up locally as well in micro-batches
The final dataset is queried from the psql client, and in this way the data is immediately present for any analysis in the psql db as well.
A docker file is created to dockerize the complete codebase
A bash file is written that sets up the env, runs lint on the code and submits the job
## Architecture and Arrangement:




## Artifacts : 
