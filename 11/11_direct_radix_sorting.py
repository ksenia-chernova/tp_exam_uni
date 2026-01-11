"""
Радикс прямая
Сортировка по разрядам. Сначала младшие (правые), потом старшие (левые)
"""

def func(arr):   
    max_num = max(arr)
    base = 10
    exp = 1

    while max_num // exp > 0:
        buckets = [[] for _ in  range(base)]

        for num in arr:
            digit = (num // exp) % base
            buckets[digit].append(num)

        arr = []
        for bucket in buckets:
            arr.extend(bucket)

        exp *= base

    return arr

array = [45, 67, 12, 23, 9, 101, 23, 13, 72, 87]
print(array)
sorted_array = func(array)
print(sorted_array)