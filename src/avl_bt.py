class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class AVL:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def update_height(self, node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        self.update_height(z)
        self.update_height(y)
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3

        self.update_height(z)
        self.update_height(y)
        return y

    def _insert(self, node, key, value):
        if not node:
            return Node(key, value)
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value
            return node
        self.update_height(node)
        balance = self.get_balance(node)
        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)
        return node

    def insert(self, key, value):
        self.root = self._insert(self.root, key, value)

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def _delete(self, node, key):
        if not node:
            return node
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                temp = node.right
                node = None
                return temp
            elif node.right is None:
                temp = node.left
                node = None
                return temp
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.value = temp.value
            node.right = self._delete(node.right, temp.key)
        if node is None:
            return node
        self.update_height(node)
        balance = self.get_balance(node)
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)
        return node

    def delete(self, key):
        self.root = self._delete(self.root, key)

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

    def _inorder(self, node, result):
        if node is not None:
            self._inorder(node.left, result)
            result.append(f"{node.key}:{node.value}")
            self._inorder(node.right, result)

    def print_inorder(self):
        result = []
        self._inorder(self.root, result)
        print(", ".join(result))

    def print_tree(self):
        print("==============")
        self._print_tree(self.root, 0)
        print("\n==============")

    def _print_tree(self, node, lvl):
        if node is not None:
            self._print_tree(node.right, lvl + 5)
            print(" " * lvl + f"{node.key}:{node.value}")
            self._print_tree(node.left, lvl + 5)

if __name__ == '__main__':
    avl = AVL()
    elements = [
        (50, 'A'), (15, 'B'), (62, 'C'), (5, 'D'), (2, 'E'), (1, 'F'),
        (11, 'G'), (100, 'H'), (7, 'I'), (6, 'J'), (55, 'K'), (52, 'L'),
        (51, 'M'), (57, 'N'), (8, 'O'), (9, 'P'), (10, 'R'), (99, 'S'),
        (12, 'T')
    ]
    for key, value in elements:
        avl.insert(key, value)
    avl.print_tree()
    avl.print_inorder()
    print(avl.search(10))
    avl.delete(50)
    avl.delete(52)
    avl.delete(11)
    avl.delete(57)
    avl.delete(1)
    avl.delete(12)
    avl.insert(3, 'AA')
    avl.insert(4, 'BB')
    avl.delete(7)
    avl.delete(8)
    avl.print_tree()
    avl.print_inorder()
