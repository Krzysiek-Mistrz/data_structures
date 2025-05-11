class ElementList:
    def __init__(self):
        self.data = None
        self.next = None
        self.prev = None


class OneDirectionList:
    def __init__(self):
        self.head = None
        self.tail = None

    #function to destroy the list
    def destroy(self):
        current = self.head
        while current:
            nxt = current.next
            current.next = None
            current.prev = None
            current = nxt
        self.head = None
        self.tail = None

    #function to add the element to the beginning of the list
    def add(self, data):
        new_elem = ElementList()
        new_elem.data = data
        new_elem.next = self.head
        new_elem.prev = None
        if self.head:
            self.head.prev = new_elem
        else:
            self.tail = new_elem
        self.head = new_elem

    #function to append the element to the end of the list
    def append(self, data):
        new_elem = ElementList()
        new_elem.data = data
        new_elem.next = None
        new_elem.prev = self.tail
        if self.tail:
            self.tail.next = new_elem
        else:
            self.head = new_elem
        self.tail = new_elem

    #function to remove the first elem from the list
    def remove(self):
        if not self.head:
            return
        next_elem = self.head.next
        self.head.next = None
        if next_elem:
            next_elem.prev = None
        else:
            self.tail = None
        self.head = next_elem

    #function to remove the element from the end of the list
    def remove_end(self):
        if not self.tail:
            return
        prev_elem = self.tail.prev
        self.tail.prev = None
        if prev_elem:
            prev_elem.next = None
        else:
            self.head = None
        self.tail = prev_elem

    #function to check if list is empty
    def is_empty(self):
        return self.head is None

    #function to count num of elems in odl
    def length(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count
    
    #function to get the first element
    def get(self):
        return None if not self.head else self.head.data

    #function to print the list
    def print_list(self):
        curr = self.head
        while curr:
            print("->", curr.data)
            curr = curr.next

    #function to print the list in reverse
    def print_list_rev(self):
        curr = self.tail
        while curr:
            print("<-", curr.data)
            curr = curr.prev


data_list = [('AGH', 'Kraków', 1919),
             ('UJ', 'Kraków', 1364),
             ('PW', 'Warszawa', 1915),
             ('UW', 'Warszawa', 1915),
             ('UP', 'Poznań', 1919),
             ('PG', 'Gdańsk', 1945)]
uczelnie = OneDirectionList()
for data in data_list[:3]:
    uczelnie.append(data)
for data in data_list[3:]:
    uczelnie.add(data)
uczelnie.print_list()
uczelnie.print_list_rev()
print(uczelnie.length())
uczelnie.remove()
print(uczelnie.get())
uczelnie.remove_end()
uczelnie.print_list()
uczelnie.print_list_rev()
uczelnie.destroy()
print(uczelnie.is_empty())
uczelnie.remove()
uczelnie.remove_end()
uczelnie.append(('AGH', 'Kraków', 1919))
uczelnie.remove_end()
print(uczelnie.is_empty())