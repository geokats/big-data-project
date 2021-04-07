import argparse
import random

NEST_PROBA = 0.1
ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
            'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
            'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
            ]

def generateValue(keyType, maxLength):
    """
    Generates a random value based on the type of the key

    Parameters:
        keyType (string): can be one of "string", "int" or "float"
        maxLength (int): the max length of a string value
    """
    if keyType == "string":
        return "".join(random.choices(ALPHABET, k=random.randrange(1, maxLength)))
    elif keyType == "int":
        return random.randrange(0, 1000)
    elif keyType == "float":
        return round(random.uniform(0, 1000), 2)


def createData(keys, nLines, nesting, nKeys, maxLength):
    """
    Generates syntactically correct data for the KV Broker

    Parameters:
        keys (string): the path to a file containing a space-separated list of keys and their data types
        nLines (int): the number of lines to generate
        nesting (int): the maximum nesting level
        nKeys (int): the maximum number of keys inside each value
        maxLength (int): the maximum length of a string value
    """
    for i in range(nLines):
        line = "\"key{}\" : ".format(i) + "{"

        for key in range(random.randrange(nKeys)):
            if key > 0:
                line += " ;"

            keyName, keyType = random.choice(list(keys.items()))

            if nesting > 0 and random.random() < NEST_PROBA:
                for data in createData(keys, 1, nesting-1, nKeys, maxLength):
                    line += data
            else:
                line += " \"{}\" : {}".format(keyName, generateValue(keyType, maxLength))

        line += " }"
        yield line

if __name__ == '__main__':
    #Parse arguments
    parser = argparse.ArgumentParser(description='Generate data for the KV Broker')
    parser.add_argument('-n', required=True, type=int, metavar='nLines',
                        help='the number of lines to generate'
                        )
    parser.add_argument('-d', required=True, type=int, metavar='nesting',
                        help='the maximum level of nesting'
                        )
    parser.add_argument('-m', required=True, type=int, metavar='nKeys',
                        help='maximum number of keys inside each value'
                        )
    parser.add_argument('-l', required=True, type=int, metavar='maxLength',
                        help='the maximum length of a string value'
                        )
    parser.add_argument('-k', required=True, type=str, metavar='keyFile',
                        help='a file containing a space-separated list of key names and their data types'
                        )
    args = parser.parse_args()


    #Read key file
    keys = {}
    with open(args.k, 'r') as f:
        for line in f:
            keyName, keyType = line.split()
            keys[keyName] = keyType

    #Generate data
    for line in createData(keys, args.n, args.d, args.m, args.l):
        print(line)
