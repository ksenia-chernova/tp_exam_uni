"""
Радикс обмен
Сортировка по разрядам. Сначала старшие (левые), потом младшие (правые)
"""

def func(arr, left=0, right=None, digit_pos=None):
    if right is None:
        right = len(arr) - 1

    if digit_pos is None:
        # Находим максимальное число для определения максимального разряда
        max_num = max(arr)
        # Определяем максимальный разряд (10^k)
        digit_pos = 1
        while max_num // digit_pos > 0:
            digit_pos *= 10
        digit_pos //= 10  # Переходим к старшему разряду
    
    if left < right and digit_pos > 0:
        # Разделение массива по текущему разряду
        i, j = left, right
        
        while i <= j:
            # Ищем элемент с 0 в текущем разряде справа
            while i <= j and (arr[i] // digit_pos) % 10 == 0:
                i += 1
            
            # Ищем элемент с не-0 в текущем разряде слева
            while i <= j and (arr[j] // digit_pos) % 10 != 0:
                j -= 1
            
            if i <= j:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
                j -= 1

        func(arr, left, j, digit_pos // 10)
        func(arr, i, right, digit_pos // 10)
    
    return arr

array = [45, 67, 12, 23, 9, 101, 23, 13, 72, 87]
print(array)
sorted_array = func(array)
print(sorted_array)