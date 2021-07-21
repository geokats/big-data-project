# Big Data Management Project: Key-Value Store

## Intorduction
This repository contains a programming assignment implemented for my Big Data Management 
class, for the MSc Data Science and Information Technologies program at the National and
Kapodistrian University of Athens.

A description of the assignment and its requirements can be found in the 
[project.pdf](project.pdf) file.

## How to run the programs

### Data Creation
The following command will generate and print the data to the command line.
A key file is needed with all the possible key names and types (string, int, float).

`python3 createData.py -n nLines -d nesting -m nKeys -l maxLength -k keyFile`

Example usage, redirecting output to a file:

`python3 createData.py -n 1000 -d 3 -m 10 -l 5 -k keyFile.txt > dataToIndex.txt`

### KV Broker
The following command starts the KV Broker, which sends the data from the
dataToIndex to the servers from the serverFile with a replication factor and
waits for commands from the user.

`python3 kvBroker.py -s serverFile -i dataToIndex -k replication`

Example usage, with a replication factor of 3:

`python3 kvBroker.py -s serverFile.txt -i dataToIndex.txt -k 3`

### KV Server
The following command starts the KV Server, which waits for data to store in
its trie from the KV Broker.
When all the data has been received, it waits for commands from the broker.

`python3 kvServer.py -a ip_address -p port`

Example usage, running at localhost:

`python3 kvServer.py -a 127.0.0.1 -p 65432`
