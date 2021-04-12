# Big Data Management Project: Key-Value Store

## How to run the programs

### Data Creation
The following command will generate and print the data to the command line. A key file is needed with all the possible key names and types (string, int, float).

`python3 createData.py -n nLines -d nesting -m nKeys -l maxLength -k keyFile`

Example usage, redirecting output to a file:

`python3 createData.py -n 1000 -d 3 -m 10 -l 5 -k keyFile.txt > dataToIndex.txt` 
