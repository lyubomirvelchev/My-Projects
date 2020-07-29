import timeit
from random import shuffle
import tracemalloc
import sys

tracemalloc.start()
sys.setrecursionlimit(2000)

recursiv_sorted_list = []

def brute_force_cyclic(lst):
    sorted_list = []
    while len(lst) != 0:
        smallest_number_idx = 0
        for next_number_idx in range(len(lst)):
            if lst[smallest_number_idx] > lst[next_number_idx]:
                smallest_number_idx = next_number_idx
        sorted_list.append(lst[smallest_number_idx])
        lst.pop(smallest_number_idx)
    return sorted_list


def brute_force_recursiv(lst):
    smallest_number_idx = 0
    for next_number_idx in range(len(lst)):
        if lst[smallest_number_idx] > lst[next_number_idx]:
            smallest_number_idx = next_number_idx
    recursiv_sorted_list.append(lst[smallest_number_idx])
    lst.pop(smallest_number_idx)
    if len(lst) != 0:
        brute_force_recursiv(lst)
    return recursiv_sorted_list

def bubble_sort(lst):
    length = len(lst)
    while length > 1:
        for buffer_idx in range(length - 1):
            if lst[buffer_idx] > lst[buffer_idx + 1]:
                lst[buffer_idx], lst[buffer_idx + 1] = lst[buffer_idx + 1], lst[buffer_idx]
        length -= 1
    return lst

def generate_random_list():
    test_list = list(range(100))
    shuffle(test_list)
    return test_list



def split_list(lst):
    pop_idx = 0
    for _ in range(int(len(lst) / 2)):
        if lst[pop_idx] > lst[pop_idx + 1]:
            lst[pop_idx], lst[pop_idx + 1] = lst[pop_idx + 1], lst[pop_idx]
        lst.append([lst[pop_idx], lst[pop_idx + 1]])
        lst.pop(pop_idx)
        lst.pop(pop_idx)
    if isinstance(lst[0], int):
        lst.append([lst[0]])
        lst.pop(pop_idx)
    return lst

def merge_sort(lst):
    while len(lst) > 1:
        for _ in range(int(len(lst)/2)):
            lst.append(merge_me(lst[0],lst[1]))
            lst.pop(0)
            lst.pop(0)
    return lst

def merge_me(lst1, lst2):
    new_list = []
    for _ in range(len(lst1) + len(lst2)):
        if len(lst1) == 0:
            for elem in lst2:
                new_list.append(elem)
            break
        elif len(lst2) == 0:
            for elem in lst1:
                new_list.append(elem)
            break
        elif lst1[0] < lst2[0]:
            new_list.append(lst1[0])
            lst1.pop(0)
        else:
            new_list.append(lst2[0])
            lst2.pop(0)
    return new_list


def test_cyclic():
    return brute_force_cyclic(generate_random_list())

def test_bubble():
    return bubble_sort(generate_random_list())

def test_merge():
    return merge_sort(split_list(generate_random_list()))

def bubble_sort2(lst):
    while True:
        changed = False
        for idx in range(len(lst)-1):
            if lst[idx] > lst[idx + 1]:
                buff = lst[idx]
                lst[idx] = lst[idx + 1]
                lst[idx + 1] = buff
                changed = True
        if not changed:
            return lst

#
# brute_force_cyclic(generate_random_list())
# bubble_sort(generate_random_list())
# merge_sort(split_list(generate_random_list()))

# snapshot = tracemalloc.take_snapshot()
# top_stats = snapshot.statistics('lineno')
#
# print("[ Top 10 ]")
# for stat in top_stats[:10]:
#     print(stat)

print(timeit.timeit("test_cyclic()",setup="from __main__ import test_cyclic",number=1000))
print(timeit.timeit("test_bubble()",setup="from __main__ import test_bubble",number=1000))
print(timeit.timeit("test_merge()",setup="from __main__ import test_merge",number=1000))
