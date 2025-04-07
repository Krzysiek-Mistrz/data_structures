class Queue:
    def __init__(self):
        self.tab = [None] * 5
        self.size = 5
        self.w_idx = 0
        self.r_idx = 0
    
    def is_empty(self):
        return self.w_idx == self.r_idx
    
    def peek(self):
        if self.is_empty():
            return None
        return self.tab[self.r_idx]
    
    def dequeue(self):
        if self.is_empty():
            return None
        elem = self.tab[self.r_idx]
        self.tab[self.r_idx] = None
        self.r_idx = (self.r_idx + 1) % self.size
        return elem
    
    def enqueue(self, new_elem):
        next_w_idx = (self.w_idx + 1) % self.size
        #sprawdzenie ograniczenia rozmiaru
        if next_w_idx == self.r_idx:
            self.resize()
        self.tab[self.w_idx] = new_elem
        self.w_idx = (self.w_idx + 1) % self.size
    
    def resize(self):
        new_size = self.size * 2
        new_tab = [None] * new_size
        if self.r_idx < self.w_idx:
            new_tab[:self.w_idx - self.r_idx] = self.tab[self.r_idx:self.w_idx]
        else:
            part1 = self.tab[self.r_idx:]
            part2 = self.tab[:self.w_idx]
            new_tab[:len(part1)] = part1
            new_tab[len(part1):len(part1) + len(part2)] = part2
        self.tab = new_tab
        self.w_idx = (self.w_idx - self.r_idx) % self.size
        self.r_idx = 0
        self.size = new_size
    
    def __str__(self):
        #elementy tylko z rozwazanego przedzialu
        elements = [self.tab[(self.r_idx + i) % self.size] for i in range((self.w_idx - self.r_idx) % self.size)]
        return str(elements)
    
    def test(self):
        return self.tab

if __name__ == "__main__":
    q = Queue()
    for i in range(1, 5):
        q.enqueue(i)
    print(q.dequeue())
    print(q.peek())
    print(q)
    for i in range(5, 9):
        q.enqueue(i)
    print(q.test())
    while not q.is_empty():
        print(q.dequeue())
    print(q)