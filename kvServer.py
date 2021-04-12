import argparse
import socket

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

    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)

    #Close socket
    s.close()
