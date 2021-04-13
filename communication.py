import random
import socket

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
            s.connect((address, port))
            s.sendall(msg.encode('utf8'))
            # reply = recvall(s)
            # print(reply)
            # if not reply == "OK":
            #     print("ERROR: Failure sending data to servers")
            #     break


def recvall(conn):
    all_data = b""
    while True:
        data = conn.recv(4096)
        if not data:
            break
        else:
            all_data += data

    return all_data
