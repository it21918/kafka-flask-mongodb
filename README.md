# Run the project
```
python3 -m venv myvenv
source myvenv/bin/activate
python -m pip install -r requirements.txt
python consumer.py
python producer.py
python postman.py
```
# RabbitMQ 
## Install rabbitMQ 
```
sudo apt-get install rabbitmq-server
```
## Start server 
```
sudo su
sudo service rabbitmq-server restart 
```

# Install and Run Kafka 3.3.1 On WSL
## Install java 
```
sudo apt update
sudo apt install default-jre
java -version
```

## Set up JAVA_HOME variable
### Setup environment variables by editing file ~/.bashrc.
```
vi ~/.bashrc
```

### Add the following environment variables:
``` 
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64
```
### save the file
```
source ~/.bashrc
```

## Download kafka
```
wget https://dlcdn.apache.org/kafka/3.3.1/kafka_2.12-3.3.1.tgz
```
### Unzip the binary package to a installation folder.
```
tar -xvzf  kafka_2.12-3.3.1.tgz
```
### Setup environment variables by editing file ~/.bashrc.
 ```
 vi ~/.bashrc
```
### Add the following environment variables:
```
export KAFKA_HOME=~/kafka_2.12-3.3.1
```
### Save the file and source the changes.
```
source ~/.bashrc
```

## Start Kafka
### Start ZooKeeper services by running this command:
```
$KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties
```
### Open another WSL terminal and run the following command:
```
$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties
```

## Shutdown kafka services
```
$KAFKA_HOME/bin/kafka-server-stop.sh $KAFKA_HOME/config/server.properties
$KAFKA_HOME/bin/zookeeper-server-stop.sh $KAFKA_HOME/config/zookeeper.properties
```
