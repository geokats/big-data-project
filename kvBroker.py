import argparse
import socket
import random

def send_repl(msg, servers, k=1):
    """
    Sends the message to random servers with a replication factor k

        Parameters:
            msg (string): The message to send
            servers (list): A list of tuples containing ip addresses and ports
            k (int): The replication factor
    """
    for address, port in random.choices(servers, k=k):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            #Send data
            s.connect((address, port))
            s.sendall(msg.encode('utf8'))
            #Wait for verification
            reply = s.recv(8192)
            if not reply == b"OK":
                print("ERROR: Failure sending data to servers")
                break

def send_stop(servers):
    """
    Sends the STOP command to all servers

        Parameters:
            servers (list): A list of tuples containing ip addresses and ports
    """
    for address, port in servers:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((address, port))
            s.sendall(b"STOP")

def send_get(cmd, servers):
    """
    Sends a GET command to all servers and gathers replies

        Parameters:
            cmd (string): A command starting with GET, without any quotation marks
            servers (list): A list of tuples containing ip addresses and ports
    """
    replies = []

    cmd = cmd.encode('utf-8')
    for address, port in servers:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((address, port))
            s.sendall(cmd)
            #Wait for reply
            reply = s.recv(8192)
            if not reply == b"NOT FOUND":
                replies.append(reply.decode('utf-8'))

    return replies

if __name__ == '__main__':
    #Parse arguments
    parser = argparse.ArgumentParser(description='Distributes data to the servers and handles user commands')
    parser.add_argument('-s', required=True, type=str, metavar='serverFile',
                        help='file containing a space separated list of server IPs and \
                        their respective ports that  be listening for queries and indexing commands'
                        )
    parser.add_argument('-i', required=True, type=str, metavar='dataToIndex',
                        help='a file containing the data to be stored'
                        )
    parser.add_argument('-k', required=True, type=int, metavar='replication',
                        help='the replication factor, i.e. how many different servers \
                        will have the same replicated data'
                        )
    args = parser.parse_args()

    #Read server server file
    servers = []
    with open(args.s, "r") as f:
        for line in f:
            line = line.rstrip("\n")
            address, port = line.split(" ")
            servers.append((address, int(port)))

    assert len(servers) <= args.k

    #Read data file and send each line to k servers
    with open(args.i, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            msg = f"PUT {line}"
            send_repl(msg, servers, k=1)

    #Send the stop command to all servers
    send_stop(servers)

    #Command Interface Loop
    stop_cmd = False
    while not stop_cmd:
        user_cmd = input("Type your command: ")
        if user_cmd == "STOP":
            send_stop(servers)
            stop_cmd = True
        elif user_cmd.startswith("GET"):
            cmd = user_cmd.replace('\"','').replace('\'','')
            result = send_get(cmd, servers)
            print(result)

        # elif user_cmd.startswith("QUERY"):
        # elif user_cmd.startswith("DELETE"):
        else:
            print("ERROR: Command not recognized")
