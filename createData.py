import random

NEST_PROBA = 0.1

def createData(keyFile, nLines, nesting, nKeys, maxLength):
    """
    Generates syntactically correct data for the KV Broker

    Parameters:
        keyFile (string): the path to a file containing a space-separated list of keys and their data types
        nLines (int): the number of lines to generate
        nesting (int): the maximum nesting level
        nKeys (int): the maximum number of keys inside each value
        maxLength (int): the maximum length of a string value
    """

    #Read key file
    keys = {"name": "string",
            "age" : "int"
            }

    for i in range(nLines):
        line = "\"key{}\" : ".format(i) + "{"

        for key in range(random.randrange(nKeys)):
            if key > 0:
                line += " ; "

            keyName, keyType = random.choice(list(keys.items()))

            if nesting > 0 and random.random() < NEST_PROBA:
                for data in createData(keyFile, nLines, nesting-1, nKeys, maxLength):
                    line += data
            else:
                line += " \"{}\" : {}".format(keyName, keyType)

        line += " }"
        yield line

if __name__ == '__main__':
    for line in createData(None, 3, 1, 5, 10):
        print(line)
