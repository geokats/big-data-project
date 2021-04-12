import argparse



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
    parser.add_argument('-k', required=True, type=int, metavar='nKeys',
                        help='the replication factor, i.e. how many different servers \
                        will have the same replicated data'
                        )
    args = parser.parse_args()
