import random
import time

class PQElem:
    def __init__(self, dane, priorytet):
        self.dane = dane
        self.priorytet = priorytet
    def __lt__(self, other):
        return self.priorytet < other.priorytet
    def __gt__(self, other):
        return self.priorytet > other.priorytet
    def __repr__(self):
        return f"{self.priorytet} : {self.dane}"

class PriorityQueue:
    def __init__(self, tab_sort=None):
        if tab_sort is not None:
            self.queue = tab_sort
            self.heap_size = len(self.queue)
            last_parent = (self.heap_size - 2) // 2
            for i in range(last_parent, -1, -1):
                self.pq_condition_down(i)
        else:
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
        self.queue[0], self.queue[self.heap_size - 1] = self.queue[self.heap_size - 1], self.queue[0]
        wynik = self.queue[self.heap_size - 1]
        self.heap_size -= 1
        self.pq_condition_down(0)
        return wynik
    def enqueue(self, elem: PQElem):
        if self.heap_size < len(self.queue):
            self.queue[self.heap_size] = elem
        else:
            self.queue.append(elem)
        self.heap_size += 1
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

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def shell_sort(arr):
    n = len(arr)
    h = n // 2
    while h > 0:
        for i in range(h, n):
            temp = arr[i]
            j = i
            while j >= h and temp < arr[j - h]:
                arr[j] = arr[j - h]
                j -= h
            arr[j] = temp
        h //= 2

def heapsort(arr):
    pq = PriorityQueue(arr)
    initial_size = pq.heap_size
    for _ in range(initial_size):
        pq.dequeue()

data = [(5,'A'), (5,'B'), (7,'C'), (2,'D'), (5,'E'), (1,'F'), (7,'G'), (5,'H'), (1,'I'), (2,'J')]
arr_ins = [PQElem(key, val) for key, val in data]
insertion_sort(arr_ins)
print(arr_ins)
ins_stable = [elem.dane for elem in arr_ins if elem.priorytet == 5]
data_order = [val for key, val in data if key == 5]
print("STABILNE" if ins_stable == data_order else "NIESTABILNE")
arr_shell = [PQElem(key, val) for key, val in data]
shell_sort(arr_shell)
print(arr_shell)
shell_stable = [elem.dane for elem in arr_shell if elem.priorytet == 5]
print("STABILNE" if shell_stable == data_order else "NIESTABILNE")
# arr_heap = [PQElem(key, val) for key, val in data]
# heapsort(arr_heap)
# print(arr_heap)

rand_list = [int(random.random() * 100) for _ in range(10000)]
arr_rand_ins = [PQElem(x, x) for x in rand_list]
arr_rand_shell = [PQElem(x, x) for x in rand_list]
arr_rand_heap = [PQElem(x, x) for x in rand_list]

t_start = time.perf_counter()
insertion_sort(arr_rand_ins)
t_stop = time.perf_counter()
print("Czas obliczen:", "{:.7f}".format(t_stop - t_start))
t_start = time.perf_counter()
shell_sort(arr_rand_shell)
t_stop = time.perf_counter()
print("Czas obliczen:", "{:.7f}".format(t_stop - t_start))
t_start = time.perf_counter()
heapsort(arr_rand_heap)
t_stop = time.perf_counter()
print("Czas obliczen:", "{:.7f}".format(t_stop - t_start))
