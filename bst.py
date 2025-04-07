class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def _search(self, node, key):
        if node is None:
            return None
        if key == node.key:
            return node.value
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)
    def search(self, key):
        return self._search(self.root, key)


    def _insert(self, node, key, value):
        if node is None:
            return Node(key, value)
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value
        return node
    def insert(self, key, value):
        self.root = self._insert(self.root, key, value)

    def _find_min(self, node):
        while node.left is not None:
            node = node.left
        return node

    def _delete(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                successor = self._find_min(node.right)
                node.key = successor.key
                node.value = successor.value
                node.right = self._delete(node.right, successor.key)
        return node
    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _inorder(self, node, result):
        if node is not None:
            self._inorder(node.left, result)
            result.append(f"{node.key} {node.value}")
            self._inorder(node.right, result)
    def print_inorder(self):
        result = []
        self._inorder(self.root, result)
        print(", ".join(result) + ",")

    def print_tree(self):
        print("==============")
        self._print_tree(self.root, 0)
        print("\n==============")
    def _print_tree(self, node, lvl):
        if node is not None:
            self._print_tree(node.right, lvl+5)
            print(" " * lvl + f"{node.key} {node.value}")
            self._print_tree(node.left, lvl+5)

    def _height(self, node):
        if node is None:
            return 0
        else:
            return 1 + max(self._height(node.left), self._height(node.right))
    def height(self):
        return self._height(self.root)

if __name__ == '__main__':
    bst = BST()
    elements = [
        (50, 'A'),
        (15, 'B'),
        (62, 'C'),
        (5, 'D'),
        (20, 'E'),
        (58, 'F'),
        (91, 'G'),
        (3, 'H'),
        (8, 'I'),
        (37, 'J'),
        (60, 'K'),
        (24, 'L')
    ]
    for key, value in elements:
        bst.insert(key, value)
    bst.print_tree()
    bst.print_inorder()
    print(bst.search(24))
    bst.insert(20, "AA")
    bst.insert(6, 'M')
    bst.delete(62)
    bst.insert(59, 'N')
    bst.insert(100, 'P')
    bst.delete(8)
    bst.delete(15)
    bst.insert(55, 'R')
    bst.delete(50)
    bst.delete(5)
    bst.delete(24)
    print(bst.height())
    bst.print_inorder()
    bst.print_tree()
