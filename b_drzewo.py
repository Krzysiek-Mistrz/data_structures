class BTreeNode:
    def __init__(self, max_children, is_leaf=True):
        self.max_children = max_children
        self.keys = []
        self.children = []
        self.is_leaf = is_leaf

    def split(self):
        mid = len(self.keys) // 2
        median = self.keys[mid]
        left_keys = self.keys[:mid]
        right_keys = self.keys[mid+1:]
        
        if self.is_leaf:
            left_children = []
            right_children = []
        else:
            left_children = self.children[:mid+1]
            right_children = self.children[mid+1:]
        
        self.keys = left_keys
        if not self.is_leaf:
            self.children = left_children
        
        new_node = BTreeNode(self.max_children, self.is_leaf)
        new_node.keys = right_keys
        if not self.is_leaf:
            new_node.children = right_children
        
        return median, new_node


class BTree:
    def __init__(self, max_children):
        self.max_children = max_children
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = BTreeNode(self.max_children, is_leaf=True)
            self.root.keys.append(key)
        else:
            result = self._insert(self.root, key)
            if result is not None:
                median, new_node = result
                new_root = BTreeNode(self.max_children, is_leaf=False)
                new_root.keys.append(median)
                new_root.children = [self.root, new_node]
                self.root = new_root

    def _insert(self, node, key):
        if node.is_leaf:
            i = 0
            while i < len(node.keys) and node.keys[i] < key:
                i += 1
            node.keys.insert(i, key)
        else:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            result = self._insert(node.children[i], key)
            if result is not None:
                median, new_child = result
                j = 0
                while j < len(node.keys) and node.keys[j] < median:
                    j += 1
                node.keys.insert(j, median)
                node.children.insert(j+1, new_child)
        if len(node.keys) == self.max_children:
            return node.split()
        else:
            return None

    def print_tree(self):
        print("==============")
        self._print_tree(self.root, 0)
        print("==============")

    def _print_tree(self, node, lvl):
        if node is not None:
            size = len(node.keys)
            children = node.children if not node.is_leaf else [None] * (size + 1)
            for i in range(size + 1):
                self._print_tree(children[i], lvl + 1)
                if i < size:
                    print(lvl * "  ", node.keys[i])


keys1 = [5, 17, 2, 14, 7, 4, 12, 1, 16, 8, 11, 9, 6, 13, 0, 3, 18, 15, 10, 19]
tree1 = BTree(4)
for key in keys1:
    tree1.insert(key)
tree1.print_tree()
tree2 = BTree(4)
for key in range(20):
    tree2.insert(key)
tree2.print_tree()
for key in range(20, 200):
    tree2.insert(key)
tree2.print_tree()
tree3 = BTree(6)
for key in range(200):
    tree3.insert(key)
tree3.print_tree()
