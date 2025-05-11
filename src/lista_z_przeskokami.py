import random

def randomLevel(p, maxLevel):
    lvl = 1
    while random.random() < p and lvl < maxLevel:
        lvl += 1
    return lvl

class SLElem:
    def __init__(self, key, data, level):
        self.key = key
        self.data = data
        self.level = level
        self.tab = [None] * level

    def __str__(self):
        return f"{self.key}:{self.data}"

class SkipList:
    def __init__(self, max_level):
        self.max_level = max_level
        self.head = SLElem(None, None, max_level)
        self.p = 0.5

    def search(self, key):
        current = self.head
        #przechodzimy do pzm 0
        for lvl in range(self.max_level - 1, -1, -1):
            while current.tab[lvl] is not None and current.tab[lvl].key < key:
                current = current.tab[lvl]
        candidate = current.tab[0]
        if candidate is not None and candidate.key == key:
            return candidate
        return None

    def insert(self, key, data):
        update = [None] * self.max_level
        current = self.head
        #znajdujemy poprzednikow dla kazdego pzm
        for lvl in range(self.max_level - 1, -1, -1):
            while current.tab[lvl] is not None and current.tab[lvl].key < key:
                current = current.tab[lvl]
            update[lvl] = current
        candidate = current.tab[0]
        if candidate is not None and candidate.key == key:
            candidate.data = data
            return
        lvl = randomLevel(self.p, self.max_level)
        new_node = SLElem(key, data, lvl)
        #wstawiamy nowy wezel
        for i in range(lvl):
            new_node.tab[i] = update[i].tab[i]
            update[i].tab[i] = new_node

    def remove(self, key):
        update = [None] * self.max_level
        current = self.head
        for lvl in range(self.max_level - 1, -1, -1):
            while current.tab[lvl] is not None and current.tab[lvl].key < key:
                current = current.tab[lvl]
            update[lvl] = current
        candidate = current.tab[0]
        if candidate is not None and candidate.key == key:
            for i in range(candidate.level):
                if update[i].tab[i] != candidate:
                    break
                update[i].tab[i] = candidate.tab[i]
        else:
            print("Brak danej")

    def __str__(self):
        result = "["
        node = self.head.tab[0]
        while node is not None:
            result += str(node) + ", "
            node = node.tab[0]
        result = result.rstrip(", ") + "]"
        return result

    def display_sl(self):
        node = self.head.tab[0]
        keys = []
        while node is not None:
            keys.append(node.key)
            node = node.tab[0]
        #wypisujemy pzm. od najw. do 0
        for lvl in range(self.max_level - 1, -1, -1):
            print(f"{lvl}  ", end=" ")
            node = self.head.tab[lvl]
            idx = 0
            while node is not None:
                while idx < len(keys) and node.key > keys[idx]:
                    print(" " * 5, end="")
                    idx += 1
                idx += 1
                print(f"{node.key:2d}:{node.data:2s}", end=" ")
                node = node.tab[lvl]
            print()

def test1():
    skip_list = SkipList(6)
    for i in range(1, 16):
        skip_list.insert(i, chr(64 + i))
    skip_list.display_sl()
    print(skip_list.search(2))
    skip_list.insert(2, 'Z')
    print(skip_list.search(2))
    skip_list.remove(5)
    skip_list.remove(6)
    skip_list.remove(7)
    print(skip_list)
    skip_list.insert(6, 'W')
    print(skip_list, end=2*'\n')

def test2():
    skip_list = SkipList(6)
    letters = [chr(64 + i) for i in range(1, 16)]
    letters = letters[::-1]
    for i, key in enumerate(range(15, 0, -1)):
        skip_list.insert(key, letters[i])
    skip_list.display_sl()
    print(skip_list.search(2))
    skip_list.insert(2, 'Z')
    print(skip_list.search(2))
    skip_list.remove(5)
    skip_list.remove(6)
    skip_list.remove(7)
    print(skip_list)
    skip_list.insert(6, 'W')
    print(skip_list, end=2*'\n')

if __name__ == "__main__":
    random.seed(42)
    test1()
    test2()
