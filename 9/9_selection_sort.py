"""
Сортировка выбором
0. [5, 3, 6, 1, 2, 4]

Берём минимальный элемент из массива (1) и меняем его местами с первым элементом
1. [1, 3, 6, 5, 2, 4]
2. [1, 2, 6, 5, 3, 4]
3. [1, 2, 3, 5, 6, 4]
и т.д.
"""

def func(arr):
    n = len(arr)
    for i in range(n-1):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

array = [45, 67, 12, 23, 9, 101, 23, 555, 13, 72, 87]
print(array)
sorted_array = func(array)
print(sorted_array)