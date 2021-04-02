class Node(object):
    """A trie node"""

    def __init__(self, key, value=None):
        super(Node, self).__init__()
        self.children = []
        self.value = None
        self.key = key[0]
        self.insert(key[1:], value)

    def insert(self, key, value):
        if len(key) == 0:
            #If the key is empty the value must be inserted in this node
            self.value = value
        elif len(self.children) == 0:
            #If this node has no children create one with the given key and value
            self.children.append(Node(key, value))
        else:
            #If the node already has children, find where the value must go
            for i, child in enumerate(self.children):
                if key[0] == child.key:
                    child.insert(key[1:], value)
                    break
                elif key[0] < child.key:
                    self.children.insert(i, Node(key, value))
                    break

    def find(self, key):
        if len(key) == 0:
            return value
        else:

        return

    def delete(self):
        return

    # def __str__(self):
    #     return

if __name__ == '__main__':
    n = Node("abc", 420)
    print(n)
