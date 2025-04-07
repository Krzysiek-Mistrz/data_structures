class MixElem(object):
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.next = None
        self.prev = None
    
    def __str__(self):
        return f"{self.key}:{self.val}"

class MixingTable(object):
    def __init__(self, size, c1 = 1, c2 = 0):
        self.tab = [None for i in range(size)]
        self.c1 = c1
        self.c2 = c2
        self.size = size
        #dla zamarkowania usunietych elementow zeby ich nie mylic
        self.marker = MixElem("marker", None)

    def mixing_function(self, key):
        total = 0
        if isinstance(key, str):
            for char in key:
                total += ord(char)
        else:
            total = key
        #modulo rozmiaru tablicy
        return total % self.size 
    
    def search(self, key):
        idx = self.mixing_function(key)
        #sondowanie kwadratowe
        i = 0; sq_probing = (idx + self.c1 * i + self.c2 * i**2) % self.size
        while i < self.size and self.tab[sq_probing] is not None:
            if self.tab[sq_probing] is not self.marker and self.tab[sq_probing].key == key:
                return self.tab[sq_probing]
            i += 1; sq_probing = (idx + self.c1 * i + self.c2 * i**2) % self.size
        return None
    
    def insert(self, key, elem):
        idx = self.mixing_function(key)
        #(h(k) + c1 * i + c2 * i^2) % N
        i = 0; first_marker = None; sq_probing = (idx + self.c1 * i + self.c2 * i**2) % self.size
        while i < self.size:
            if self.tab[sq_probing] is None:
                if first_marker is not None:
                    self.tab[first_marker] = MixElem(key, elem)
                else:
                    self.tab[sq_probing] = MixElem(key, elem)
                return
            elif self.tab[sq_probing] is self.marker:
                if first_marker is None:
                    first_marker = sq_probing
            elif self.tab[sq_probing].key == key:
                self.tab[sq_probing].val = elem
                return
            i += 1; sq_probing = (idx + self.c1 * i + self.c2 * i**2) % self.size
        print("Brak miejsca")
    
    def remove(self, key):
        idx = self.mixing_function(key)
        #(h(k) + c1 * i + c2 * i^2) % N
        i = 0; sq_probing = (idx + self.c1 * i + self.c2 * i**2) % self.size
        while i < self.size and self.tab[sq_probing] is not None:
            if self.tab[sq_probing] is not self.marker and self.tab[sq_probing].key == key:
                self.tab[sq_probing] = self.marker
                return
            i += 1; sq_probing = (idx + self.c1 * i + self.c2 * i**2) % self.size
        print("Brak danej")
    
    def __str__(self):
        result = "{"
        for elem in self.tab:
            if elem is not None and elem is not self.marker:
                result += f"{elem.key}:{elem.val}, "
            else:
                result += "None, "
        result = result[:-2] + " }"
        return result
    

def test1(size, c1=1, c2=0):
    table = MixingTable(size, c1, c2)
    for i in range(1, 16):
        if i == 6:
            key = 18
        elif i == 7:
            key = 31
        else:
            key = i
        table.insert(key, chr(64 + i))
    print(table)
    print(table.search(5))
    print(table.search(14))
    table.insert(5, 'Z')
    print(table.search(5))
    table.remove(5)
    print(table)
    print(table.search(31))
    #rozwiazanie za pomoca markera (nie przerywamy sondowania)
    table.insert("test", 'W')
    print(table, end='\n\n')

def test2(size, c1=1, c2=0):
    table = MixingTable(size, c1, c2)
    for i in range(1, 16):
        key = 13 * i
        table.insert(key, chr(64 + i))
    print(table, end='\n\n')

if __name__ == "__main__":
    test1(13, 1, 0)
    test2(13, 1, 0)
    test2(13, 0, 1)
    test1(13, 0, 1)
