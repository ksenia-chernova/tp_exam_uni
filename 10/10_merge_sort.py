"""
Сортировка слиянием (Merge Sort)
Исходный массив: [45, 67, 12, 23, 9, 101, 23, 13, 72, 87]

Алгоритм работает по принципу "разделяй и властвуй":
1. Разделяем массив пополам до тех пор, пока не получим массивы из одного элемента
2. Сливаем отсортированные массивы обратно в один отсортированный массив

Пример для массива [45, 67, 12, 23, 9, 101, 23, 13, 72, 87]:

Разделение:
[45, 67, 12, 23, 9] и [101, 23, 13, 72, 87]
[45, 67, 12] и [23, 9] | [101, 23, 13] и [72, 87]
[45, 67] и [12] | [23] и [9] | [101, 23] и [13] | [72] и [87]
[45] и [67] | [12] | [23] | [9] | [101] и [23] | [13] | [72] | [87]

Слияние:
[45, 67] ← [45] + [67]
[12, 45, 67] ← [12] + [45, 67]
[9, 23] ← [9] + [23]
[9, 12, 23, 45, 67] ← [9, 23] + [12, 45, 67]
[23, 101] ← [23] + [101]
[13, 23, 101] ← [13] + [23, 101]
[72, 87] ← [72] + [87]
[13, 23, 72, 87, 101] ← [13, 23, 101] + [72, 87]
[9, 12, 13, 23, 23, 45, 67, 72, 87, 101] ← [9, 12, 23, 45, 67] + [13, 23, 72, 87, 101]
"""

def func(arr):
    
    if len(arr) <= 1:
        return arr
    
    middle = len(arr) // 2
    left = arr[:middle]
    right = arr[middle:]

    left_sorted = func(left)
    right_sorted = func(right)

    return merge(left_sorted, right_sorted)

def merge(left, right):

    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    while i < len(left):
        result.append(left[i])
        i += 1

    while j < len(right):
        result.append(right[j])
        j += 1

    return result

array = [45, 67, 12, 23, 9, 101, 23, 13, 72, 87]
print(array)
sorted_array = func(array)
print(sorted_array)