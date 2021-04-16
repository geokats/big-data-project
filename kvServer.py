import argparse
import socket
import json
from trie import Node

def parseKV(kv):
    """
    Parses a key-value pair by converting it into json format and using python's
    json libarary
        Parameters:
            kv (string): A string describing a key-value pair as is defined for
                the means of this project
        Returns:
            key (string): the key of the key-value pair
            value : the value of the key-value pair in its appropriate type
    """
    j = kv.replace(";",",")
    d = json.loads("{{{}}}".format(j))
    assert len(d) == 1
    key, value = list(d.items())[0]
    return key, value

if __name__ == '__main__':
    #Parse arguments
    parser = argparse.ArgumentParser(description='Stores data and serves queries coming from the KV Broker')
    parser.add_argument('-a', required=True, type=str, metavar='ip_address',
                        help='KV server\'s IP address'
                        )
    parser.add_argument('-p', required=True, type=int, metavar='port',
                        help='KV server\'s port'
                        )
    args = parser.parse_args()

    #Initialize Trie KV Store
    #The base trie has no value and will contain all the received KVs as tries
    store = Node(key="server")

    #Create and bind socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((args.a, args.p))
    s.listen()

    #Set-up phase
    stop_cmd = False
    while not stop_cmd:
        conn, addr = s.accept()
        with conn:
            #Receive message
            print(f'{10*"="} Connected to {addr} {10*"="}')
            data = conn.recv(8192)
            msg = data.decode('utf-8')
            print(msg)

            if msg == "STOP":
                stop_cmd = True
            elif msg.startswith("PUT"):
                #Parse the data
                key, values = parseKV(msg[4:])
                print(f"Adding: {key}:{values}")
                #Insert data to the trie
                store.insert(key, values)
                #Send verification to kvBroker
                conn.sendall(b"OK")
            else:
                conn.sendall(b"ERROR")

    #Command phase
    stop_cmd = False
    while not stop_cmd:
        conn, addr = s.accept()
        with conn:
            #Receive message
            print(f'{10*"="} Connected to {addr} {10*"="}')
            data = conn.recv(8192)
            msg = data.decode('utf-8')
            print(msg)

            if msg == "STOP":
                stop_cmd = True
            elif msg == "CHECK":
                #If the broker checks for the server's availability, reply with OK
                conn.sendall(b"OK")
            elif msg.startswith("GET"):
                #Look if the key exists as a top-level key only
                key = msg.lstrip("GET ")
                result = store.find(key)
                if result is None:
                    reply = b"NOT FOUND"
                else:
                    reply = f"{key} : {result}".encode('utf-8')
                conn.sendall(reply)

            elif msg.startswith("QUERY"):
                #Split the key into subkeys and check for each subkey while moving deeper
                key = msg.lstrip("QUERY ")
                subkeys = key.split(".")

                n = store
                for sk in subkeys:
                    if not isinstance(n, Node):
                        n = None
                        break
                    n = n.find(sk)
                result = n
                if result is None:
                    reply = b"NOT FOUND"
                else:
                    reply = f"{key} : {result}".encode('utf-8')
                conn.sendall(reply)

            elif msg.startswith("DELETE"):
                #If the key is found and deleted reply with OK, otherwise NOT FOUND
                key = msg.lstrip("DELETE ")
                if store.delete(key):
                    conn.sendall(b"OK")
                else:
                    conn.sendall(b"NOT FOUND")
            else:
                conn.sendall(b"ERROR")

    #Close socket
    s.close()
