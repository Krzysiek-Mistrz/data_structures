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

    def print_tab(self):
        print('{', end=' ')
        print(*self.queue[:self.heap_size], sep=', ', end=' ')
        print('}')

    def print_tree(self, idx=0, lvl=0):
        if idx < self.heap_size:
            self.print_tree(self.right(idx), lvl + 1)
            print('  ' * lvl + str(self.queue[idx]))
            self.print_tree(self.left(idx), lvl + 1)


def selection_sort_swap(arr):
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i+1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        if i != min_index:
            arr[i], arr[min_index] = arr[min_index], arr[i]

def selection_sort_shift(arr):
    n = len(arr)
    i = 0
    while i < n:
        min_index = i
        for j in range(i+1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        element = arr.pop(min_index)
        arr.insert(i, element)
        i += 1


if __name__ == '__main__':
    decision = int(input())

    #test 1
    if decision == 1:
        data = [(5, 'A'), (5, 'B'), (7, 'C'), (2, 'D'), (5, 'E'),
                (1, 'F'), (7, 'G'), (5, 'H'), (1, 'I'), (2, 'J')]
        elem_list = [PQElem(key, val) for key, val in data]
        pq = PriorityQueue(elem_list[:])
        print(pq.queue)
        pq.print_tree()
        initial_size = pq.heap_size
        for _ in range(initial_size):
            pq.dequeue()
        print(pq.queue)
        orig_order = [val for key, val in data if key == 5]
        sorted_order = [elem.dane for elem in pq.queue if elem.priorytet == 5]
        if sorted_order == orig_order:
            print("STABILNE")
        else:
            print("NIESTABILNE")

        arr_sel_swap = [PQElem(key, val) for key, val in data]
        selection_sort_swap(arr_sel_swap)
        print(arr_sel_swap)
        stable_order_swap = [elem.dane for elem in arr_sel_swap if elem.priorytet == 5]
        if stable_order_swap == [val for key, val in data if key == 5]:
            print("STABILNE")
        else:
            print("NIESTABILNE")
        arr_sel_shift = [PQElem(key, val) for key, val in data]
        selection_sort_shift(arr_sel_shift)
        print(arr_sel_shift)
        stable_order_shift = [elem.dane for elem in arr_sel_shift if elem.priorytet == 5]
        if stable_order_shift == [val for key, val in data if key == 5]:
            print("STABILNE")
        else:
            print("NIESTABILNE")
    
    elif decision == 2:
        random_list_sel = [int(random.random() * 100) for _ in range(10000)]
        random_list_sel_cp1 = random_list_sel[:]
        random_list_sel_cp2 = random_list_sel[:]
        arr_sel_rand = random_list_sel[:]
        t_start = time.perf_counter()
        selection_sort_swap(arr_sel_rand)
        t_stop = time.perf_counter()
        print("Czas obliczen:", "{:.7f}".format(t_stop - t_start))
        arr_sel_rand2 = random_list_sel_cp1[:]
        t_start = time.perf_counter()
        selection_sort_shift(arr_sel_rand2)
        t_stop = time.perf_counter()
        print("Czas obliczen:", "{:.7f}".format(t_stop - t_start))
        random_arr = [PQElem(x, x) for x in random_list_sel_cp2]
        pq_random = PriorityQueue(random_arr[:])
        t_start = time.perf_counter()
        for _ in range(len(random_arr)):
            pq_random.dequeue()
        t_stop = time.perf_counter()
        print("Czas obliczen:", "{:.7f}".format(t_stop - t_start))