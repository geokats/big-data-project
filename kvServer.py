import argparse
import socket

stop_cmd = False

def recvall(conn):
    all_data = b""
    while True:
        data = conn.recv(4096)
        if not data:
            break
        else:
            all_data += data

    return all_data

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

    #Create and bind socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((args.a, args.p))
    s.listen()

    while not stop_cmd:
        conn, addr = s.accept()
        with conn:
            #Receive message
            print(f'Connected to {addr}')
            data = recvall(conn)
            msg = data.decode('utf-8')
            print(msg)

            if msg == "STOP":
                stop_cmd = True
            elif msg.startswith("PUT"):
                entry = msg[4:]
                print(f"Adding: {entry}")


    #Close socket
    s.close()
