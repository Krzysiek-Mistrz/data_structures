class PQElem:
    def __init__(self, dane, priorytet):
        self.__dane = dane
        self.__priorytet = priorytet

    def __lt__(self, other):
        return self.__priorytet < other.__priorytet

    def __gt__(self, other):
        return self.__priorytet > other.__priorytet

    def __repr__(self):
        return f"{self.__priorytet} : {self.__dane}"


class PriorityQueue:
    def __init__(self):
        #queue[0] to nasz root
        self.queue = []
        self.heap_size = 0

    def is_empty(self):
        return self.heap_size == 0

    def peek(self):
        if self.is_empty():
            return None
        return self.queue[0]

    def dequeue(self):
        if self.is_empty():
            return None
        max_elem = self.queue[0]
        self.queue[0] = self.queue[self.heap_size - 1]
        self.heap_size -= 1
        #przywracamy wl kopca od zdjetego roota w dol
        self.pq_condition_down(0)
        return max_elem

    def enqueue(self, elem: PQElem):
        if self.heap_size < len(self.queue):
            self.queue[self.heap_size] = elem
        else:
            self.queue.append(elem)
        self.heap_size += 1
        #przywracamy wl kopca od wstawionego elem w gore
        self.pq_condition_up(self.heap_size - 1)

    def pq_condition_up(self, index):
        while index > 0:
            parent_index = self.parent(index)
            if parent_index is not None and self.queue[index] > self.queue[parent_index]:
                self.queue[index], self.queue[parent_index] = self.queue[parent_index], self.queue[index]
                index = parent_index
            else:
                break

    def pq_condition_down(self, index):
        while True:
            left_index = self.left(index)
            right_index = self.right(index)
            largest = index
            if left_index < self.heap_size and self.queue[left_index] > self.queue[largest]:
                largest = left_index
            if right_index < self.heap_size and self.queue[right_index] > self.queue[largest]:
                largest = right_index
            if largest != index:
                self.queue[index], self.queue[largest] = self.queue[largest], self.queue[index]
                index = largest
            else:
                break

    def left(self, idx):
        return 2 * idx + 1

    def right(self, idx):
        return 2 * idx + 2

    def parent(self, idx):
        if idx == 0:
            return None
        return (idx - 1) // 2

    def print_tab(self):
        print('{', end=' ')
        print(*self.queue[:self.heap_size], sep=', ', end=' ')
        print('}')

    def print_tree(self, idx, lvl):
        if idx < self.heap_size:
            self.print_tree(self.right(idx), lvl + 1)
            print('  ' * lvl, self.queue[idx])
            self.print_tree(self.left(idx), lvl + 1)


priorities = [7, 5, 1, 2, 5, 3, 4, 8, 9]
values = "GRYMOTYLA"
pq = PriorityQueue()
for p, v in zip(priorities, values):
    elem = PQElem(v, p)
    pq.enqueue(elem)
pq.print_tree(0, 0)
pq.print_tab()
removed = pq.dequeue()
print(removed)
print(pq.peek())
pq.print_tab()
print(removed)
while not pq.is_empty():
    print(pq.dequeue())
print()
pq.print_tab()