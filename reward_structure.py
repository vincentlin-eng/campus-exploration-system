# Note: This file is used for Task 4.4 only
from __future__ import annotations
from data_structures.referential_array import ArrayR
from data_structures.array_max_heap import ArrayMaxHeap
from data_structures.abstract_heap import AbstractHeap, T

class RewardStructure(ArrayMaxHeap[T]):
    def __init__(self, max_items = 1):
        ArrayMaxHeap.__init__(self, max_items)

    def resize(self):
        old_capacity = len(self._array) - 1
        new_capacity = old_capacity * 2 + 1
        new_array = ArrayR[T](new_capacity)

        for i in range(1, self._length + 1):
            new_array[i] = self._array[i]
        
        self._array = new_array

    def add(self, item:T):
        if self.is_full():
            self.resize()

        ArrayMaxHeap.add(self, item)


    


