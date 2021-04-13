import argparse
import socket
import json
from trie import Node
from communication import recvall

stop_cmd = False

def parseKV(kv):
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

    #KeyValue insertion phase
    while not stop_cmd:
        conn, addr = s.accept()
        with conn:
            #Receive message
            print(f'{10*"="} Connected to {addr} {10*"="}')
            data = recvall(conn)
            msg = data.decode('utf-8')
            print(msg)

            if msg == "STOP":
                stop_cmd = True
            elif msg.startswith("PUT"):
                key, values = parseKV(msg[4:])
                print(f"Adding: {key}:{values}")
                store.insert(key, values)
                # conn.sendall(b"OK")


    #Close socket
    s.close()
