"""
Сортировка пузырьком
0. [4, 3, 1, 2, 7, 3]
1. [_3, 4_, 1, 2, 7, 3]
2. [3, _1, 4_, 2, 7, 3]
3. [3, 1, _2, 4_, 7, 3]
4. [3, 1, 2, _4, 7_, 3]
5. [3, 1, 2, 4, _3, 7_]

и так проходимся много раз по массиву до тех пор, пока он не будет отсортирован

"""

def func(arr):
    n = len(arr)
    for i in range(n-1):
        flag = False
        for j in range(n-1-i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                flag = True
        if not flag:
            break
    return arr

array = [45, 67, 12, 23, 9, 101, 23, 555, 13, 72, 87]
print(array)
sorted_array = func(array)
print(sorted_array)