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
            if isinstance(value, dict):
                #If the value is a dictionary, we must construct a sub-trie
                n = Node(key="")
                for nk, nv in value.items():
                    n.insert(nk, nv)

                self.value = n
            else:
                #If the value is not a dictionary we can just insert it
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
                elif i == len(self.children) - 1:
                    #If we reached the end of the loop we must insert at the end
                    newNode = Node(key[0])
                    newNode.insert(key[1:], value)
                    self.children.append(newNode)
                    break

    def find(self, key):
        if len(key) == 0:
            return self.value
        else:
            for child in self.children:
                if key[0] == child.key:
                    return child.find(key[1:])
        return None

    def delete(self, key):
        if len(key) == 0:
            self.value = None
        else:
            for child in self.children:
                if key[0] == child.key:
                    return child.delete(key[1:])

    # def __str__(self):
    #     return

if __name__ == '__main__':
    n = Node("")
    n.insert("abc", 42)
    n.insert("abc", 22)
    n.insert("abcd", {"key1": 1, "key2": "aaa", "key3": 20.2})
    n.insert("la", {"key": 1, "ke": {"foo":100}})

    print(n.find("abc"))
    n.delete("abc")
    print(n.find("abc"))

    print(n.find("abcd"))
    print(n.find("abcd").find("key1"))
    print(n.find("abcd").find("key2"))
    print(n.find("abcd").find("key3"))
    print(n.find("la").find("ke").find("foo"))
