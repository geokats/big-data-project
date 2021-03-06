class Node(object):
    """A trie node"""

    def __init__(self, key, value=None):
        """
        Initialize the trie node.
            Parameters:
                key (string): The key of the node is a single character. If a longer
                    key is used, errors might be caused. A root node can have a longer
                    key because it is never used.
                value: The value that the node will store.
        """
        super(Node, self).__init__()
        self.children = []
        self.key = key
        self.value = value

    def insert(self, key, value):
        """
        Insert a key-value instance in the trie. If the key is an empty string,
        the value  is inserted in this node. Otherwise, the value will be recurrently
        propagated deeper in the trie until each letter of the key is assigned to
        a node and the deepest node will contain the value.
        If the value is a dictionary, a new trie will be created containing
        the key-value pairs of the dictionary. The new trie will be assigned
        as a value at the appropriate node.
            Parameters:
                key (string): The key under which the value will be stored
                value: The value that the trie will store.
        """
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
        """
        Searches for the given key in the trie. If the key is an empty string
        then the value of the current node is returned. Otherwise the first letter
        of the key is searched in the node's children and the rest of the key
        is searched recurrently in the appropriate child.
            Parameters:
                key (string): The key to search for.
            Return:
                None if the value is not found, otherwise returns the corresponding
                value
        """
        if len(key) == 0:
            return self.value
        else:
            for child in self.children:
                if key[0] == child.key:
                    return child.find(key[1:])
        return None

    def delete(self, key):
        """
        Searches for the given key in the trie and sets its value to None.
        Works similarly to the Node.find() method
            Parameters:
                key (string): The key to delete.
            Return:
                True if the value was found and deleted, otherwise False
        """
        if len(key) == 0:
            if self.value != None:
                self.value = None
                return True
            else:
                return False
        else:
            for child in self.children:
                if key[0] == child.key:
                    return child.delete(key[1:])
        return False

    def _print(self, key_prefix):
        """
        A reccurrent helping method for creating a string representation of the
        trie
            Parameters:
                key_prefix (string): The key gathered from the previously
                    traversed nodes
            Return:
                ret (dictionary): A dictionary containing all the key-value
                pairs of the node
                ret_str (string): A printable string version of the afforementioned
                dictionary
        """
        ret = {}
        cur_key = key_prefix + self.key

        if self.value != None:
            if isinstance(self.value, Node):
                ret[cur_key] = str(self.value)
            else:
                ret[cur_key] = self.value

        for child in self.children:
            child_ret, child_ret_str = child._print(cur_key)
            ret.update(child_ret)

        ret_str = "{"
        for i, (key, val) in enumerate(ret.items()):
            if i != 0:
                ret_str += " ; "
            ret_str += f"{key} : {val}"
        ret_str += "}"

        return ret, ret_str

    def __str__(self):
        """
        Return a printable string representation of the trie, using the
        reccurent Node._print() method
        """
        ret, ret_str = self._print("")
        return ret_str

if __name__ == '__main__':
    n = Node("")
    n.insert("abc", 42)
    n.insert("abc", 22)
    n.insert("abcd", {"key1": 1, "key2": "aaa", "key3": 20.2})
    n.insert("la", {"key": 1, "ke": {"foo":100, "empty": {}}})

    print(n.find("abc"))
    print(n.delete("abc"))
    print(n.delete("aabc"))
    print(n.find("abc"))

    print(n.find("abcd"))
    print(n.find("abcd").find("key1"))
    print(n.find("abcd").find("key2"))
    print(n.find("abcd").find("key3"))
    print(n.find("la").find("ke").find("foo"))
    print(n)
