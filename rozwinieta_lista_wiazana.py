BLOCK_SIZE = 6
HALF = (BLOCK_SIZE + 1) // 2

#elem of ULL list
class ULLElem(object):
    def __init__(self):
        self.arr = []
        self.num_elems = 0
        self.next = None

    def remove(self, idx):
        del self.arr[idx]
        self.num_elems -= 1

    def insert(self, idx, elem):
        self.arr = self.arr[:idx] + [elem] + self.arr[idx:]
        self.num_elems += 1

#ULL -> unrolled linked list
class ULL(object):
    def __init__(self):
        self.head = None
        self.size = 0

    def get(self, idx):
        if idx < 0 or idx >= self.size:
            raise IndexError()
        current = self.head
        pos = idx
        #moving through ULL and returning elem of last compatible pos of certain elem
        while current is not None:
            if pos < current.num_elems:
                return current.arr[pos]
            pos -= current.num_elems
            current = current.next
        raise IndexError()

    def insert(self, idx, value):
        if self.head is None:
            self.head = ULLElem()
        if idx > self.size:
            idx = self.size
        current = self.head
        prev = None
        pos = idx
        #going to certain position through elems
        while current is not None:
            if pos <= current.num_elems:
                break
            pos -= current.num_elems
            prev = current
            if current.next is None:
                break
            current = current.next
        #insert with moving existing elems within elem
        if current.num_elems < BLOCK_SIZE:
            current.insert(pos, value)
        #insert with displacement between 2 diff elems within ULL
        else:
            new_elem = ULLElem()
            split_index = current.num_elems // 2
            new_elem.arr = current.arr[split_index:]
            new_elem.num_elems = len(new_elem.arr)
            current.arr = current.arr[:split_index]
            current.num_elems = len(current.arr)
            new_elem.next = current.next
            current.next = new_elem
            if pos <= current.num_elems:
                current.insert(pos, value)
            else:
                new_pos = pos - current.num_elems
                new_elem.insert(new_pos, value)
        self.size += 1

    def delete(self, idx):
        if idx < 0 or idx >= self.size:
            raise IndexError()
        current = self.head
        prev = None
        pos = idx
        #finding first comaptible pos to delete
        while current is not None:
            if pos < current.num_elems:
                break
            pos -= current.num_elems
            prev = current
            current = current.next
        current.remove(pos)
        self.size -= 1
        #checking current elem of ULL for size below half
        if current.num_elems < HALF and current.next is not None:
            needed = HALF - current.num_elems
            if current.next.num_elems - needed < HALF:
                current.arr.extend(current.next.arr)
                current.num_elems += current.next.num_elems
                current.next = current.next.next
            else:
                transfer = min(needed, current.next.num_elems)
                current.arr.extend(current.next.arr[:transfer])
                current.num_elems += transfer
                current.next.arr = current.next.arr[transfer:]
                current.next.num_elems -= transfer

    def print_ull(self):
        elems = []
        current = self.head
        while current is not None:
            elems.extend(current.arr)
            current = current.next
        print(elems)


ull = ULL()
for i in range(1, 10):
    ull.insert(ull.size, i)
print(ull.get(4))
ull.insert(1, 10)
ull.insert(8, 11)
ull.print_ull()
ull.delete(1)
ull.delete(2)
ull.print_ull()