class ElementList(object):
    def __init__(self):
        self.data = None
        self.next = None


class OneDirectionList(object):
    def __init__(self):
        self.head = None

    #function to destroy the list
    def destroy(self):
        self.head = None

    #function to add the element to the beginning of the list
    def add(self, data):
        new_elem = ElementList()
        new_elem.data = data
        new_elem.next = self.head
        self.head = new_elem

    #function to append the element to the end of the list
    def append(self, data):
        new_elem = ElementList()
        new_elem.data = data
        if self.head is None:
            self.head = new_elem
            return
        last = self.head
        #goin to the end of the list to append the new element
        while last.next:
            last = last.next
        last.next = new_elem

    #function to remove the first elem from the list
    def remove(self):
        if self.head is None:
            return
        self.head = self.head.next

    #function to remove the element from the end of the list
    def remove_end(self):
        if self.head is None:
            return
        if self.head.next is None:
            self.head = None
            return
        current = self.head
        while current.next.next:
            current = current.next
        current.next = None

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
        if self.head is None:
            return None
        return self.head.data
    
    def print_list(self):
        current = self.head
        while current:
            print("-> ", current.data)
            current = current.next


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
print(uczelnie.length())
uczelnie.remove()
print(uczelnie.get())
uczelnie.remove_end()
uczelnie.print_list()
uczelnie.destroy()
print(uczelnie.is_empty())
uczelnie.remove()
uczelnie.remove_end()
uczelnie.append(('AGH', 'Kraków', 1919))
uczelnie.remove_end()
print(uczelnie.is_empty())