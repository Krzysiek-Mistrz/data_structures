# Heap and Sorting Algorithms

A small Python library demonstrating:
- A **Priority Queue** (max-heap) implementation  
- **Heap Sort**  
- **Shell Sort**  
- many others ;)  

---

## Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [Repository Structure](#repository-structure)  
4. [Installation](#installation)  
5. [Usage](#usage)  
   - [Priority Queue](#priority-queue)  
   - [Heap Sort](#heap-sort)  
   - [Shell Sort](#shell-sort)  
6. [Examples](#examples)  
7. [Contributing](#contributing)  
8. [License](#license)  

---

## Overview

This project provides classic data-structure and algorithm implementations for educational purposes:
- **PriorityQueue**: a max-heap supporting `enqueue`, `dequeue`, and peek.  
- **Heap Sort**: builds a heap in-place from an existing list, then sorts it.  
- **Shell Sort**: an in-place comparison sort using gap sequences.
- ...  

All implementations are pure Python, requiring no external dependencies.

---

## Features

- `PQElem`: wraps any value with an integer priority.  
- `PriorityQueue`:  
  - `enqueue(elem)`, `dequeue()`, `peek()`, `is_empty()`  
  - `print_tab()`, `print_tree()` for text visualization  
- `sortowanie_kopcowanie.py`: in-place heap sort of lists of `PQElem` or native Python orderable items.  
- `sortowanie_shella.py`: classical shell sort.  

---

## Repository Structure

```
/
├── README.md
├── LICENSE
└── src
    ├── kopiec.py                  # PriorityQueue + PQElem definitions
    ├── sortowanie_kopcowanie.py   # Heap build + heap sort
    ├── sortowanie_shella.py       # Shell sort
    └── [others algorithms & add. files]
```

---

## Installation

No special installation is required. Just clone the repository:

```bash
git clone git@github.com:Krzysiek-Mistrz/data_structures.git
cd data_structures
```

Ensure you have Python 3.6 or newer.

---

## Example usage

### Priority Queue

```python
from kopiec import PQElem, PriorityQueue

# Create queue
pq = PriorityQueue()

# Enqueue items
pq.enqueue(PQElem("task1", 5))
pq.enqueue(PQElem("task2", 2))
pq.enqueue(PQElem("task3", 9))

# Peek at max
print(pq.peek())           # => 9 : task3

# Dequeue all
while not pq.is_empty():
    print(pq.dequeue())
```

### Heap Sort

```python
from sortowanie_kopcowanie import PriorityQueue, PQElem

# Prepare list of PQElem
data = [PQElem("A", 3), PQElem("B", 1), PQElem("C", 2)]
pq = PriorityQueue(tab_sort=data)

# Dequeue in sorted order
sorted_list = []
while not pq.is_empty():
    sorted_list.append(pq.dequeue())

print(sorted_list)  # descending by priority
```

### Shell Sort

```python
from sortowanie_shella import PriorityQueue

# Shell sort works on native types or PQElem if __gt__/__lt__ are defined
arr = [5, 2, 9, 1, 5, 6]
pq = PriorityQueue(tab_sort=arr)
# After init, queue is heapified but you can call dequeue repeatedly
# or adapt code to extract sorted array.
```

---

## Examples

1. Visualize heap in tree form:
   ```python
   from kopiec import PQElem, PriorityQueue

   pq = PriorityQueue()
   for i, p in enumerate([3, 7, 1, 9]):
       pq.enqueue(PQElem(f"item{i}", p))
   pq.print_tree()
   ```

2. Compare performance of heap sort vs. shell sort on random data:
   ```python
   import random, time
   from sortowanie_kopcowanie import PriorityQueue as HeapPQ
   from sortowanie_shella import PriorityQueue as ShellPQ

   data = [random.randint(0,1000) for _ in range(10000)]

   # Heap sort benchmark
   start = time.time()
   hp = HeapPQ(tab_sort=data.copy())
   while not hp.is_empty():
       hp.dequeue()
   print("Heap sort:", time.time() - start)

   # Shell sort benchmark
   start = time.time()
   sp = ShellPQ(tab_sort=data.copy())
   # extract or ignore, but init builds heap for shell implementation
   print("Shell init (heapify):", time.time() - start)
   ```

---

## Contributing

1. Fork the repo  
2. Create a feature branch  
3. Submit a pull request  

Please follow existing code style (PEP 8 + Polish naming conventions in comments) and include tests for new features.

---

## License

GNU GPL V3 @ Krzychu 2025