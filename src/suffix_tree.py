from collections import defaultdict

class SuffixTreeNode:
    def __init__(self):
        self.children = dict()
        self.indexes = []

class SuffixTree:
    def __init__(self, text):
        self.root = SuffixTreeNode()
        self.text = text
        self.build_suffix_tree()

    def build_suffix_tree(self):
        for i in range(len(self.text)):
            current = self.root
            suffix = self.text[i:]
            for char in suffix:
                if char not in current.children:
                    current.children[char] = SuffixTreeNode()
                current = current.children[char]
                current.indexes.append(i)

    def search(self, pattern):
        current = self.root
        for char in pattern:
            if char in current.children:
                current = current.children[char]
            else:
                return 0
        return len(current.indexes)

    def print_tree(self, node=None, prefix=''):
        if node is None:
            node = self.root
        if prefix:
            print(f"{prefix}; sufixes staring on pos.: {node.indexes}")
        for char, child in node.children.items():
            self.print_tree(child, prefix + char)

def build_suffix_array(text):
    suffixes = [(text[i:], i) for i in range(len(text))]
    suffixes.sort()
    return [index for (suffix, index) in suffixes]

def binary_search_pattern(text, pattern, suffix_array):
    left, right = 0, len(suffix_array) - 1
    while left <= right:
        mid = (left + right) // 2
        start = suffix_array[mid]
        substring = text[start:start+len(pattern)]
        if pattern == substring:
            return True
        elif pattern < substring:
            right = mid - 1
        else:
            left = mid + 1
    return False

text = "banana\0"

print("Suffix tree for 'banana\\0':")
tree = SuffixTree(text)
tree.print_tree()
print()

patterns = ["ana", "na", "nan", "ban", "x"]
print("Appearances in suffix tree: ")
for p in patterns:
    count = tree.search(p)
    print(f"  '{p}': {count}")
print()

suffix_array = build_suffix_array(text)
print("Suffix table indexes: ")
print(suffix_array)
print()

print("Searching patters: ")
for p in patterns:
    found = binary_search_pattern(text, p, suffix_array)
    print(f"  '{p}': {'Found' if found else 'Cannot find'}")