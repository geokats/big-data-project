class Node(object):
    """A trie node"""

    def __init__(self, key, value=None):
        super(Node, self).__init__()
        self.children = []
        self.key = key
        self.value = value

    def insert(self, key, value):
        if len(key) == 0:
            #If the key is empty the value must be inserted in this node
            self.value = value
        elif len(self.children) == 0:
            #If this node has no children create one with the given key and value
            newNode = Node(key[0])
            newNode.insert(key[1:], value)
            self.children.append(newNode)
        else:
            #If the node already has children, find where the value must go
            for i, child in enumerate(self.children):
                if key[0] == child.key:
                    child.insert(key[1:], value)
                    break
                elif key[0] < child.key:
                    newNode = Node(key[0])
                    newNode.insert(key[1:], value)
                    self.children.insert(i, newNode)
                    break

    def find(self, key):
        if len(key) == 0:
            return self.value
        else:
            for child in self.children:
                if key[0] == child.key:
                    return child.find(key[1:])
        return None

    def delete(self):
        return

    # def __str__(self):
    #     return

if __name__ == '__main__':
    n = Node("")
    n.insert("abc", 420)
    n.insert("abcd", Node(""))
    print(n.find("abc"))
    print(n.find("abcd"))
