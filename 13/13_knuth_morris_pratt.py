"""
Кнут-Моррис-Пратт
"""

def build_prefix_function(pattern):
    """
    Построение префикс-функции для паттерна
    
    Префикс-функция π[i] = длина наибольшего собственного суффикса
    подстроки pattern[0..i], который одновременно является префиксом.
    
    Собственный суффикс = суффикс, не совпадающий со всей строкой.
    """
    m = len(pattern)
    prefix = [0] * m  # префикс-функция
    
    # Длина предыдущего наибольшего префикса-суффикса
    length = 0
    i = 1
    
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            prefix[i] = length
            i += 1
        else:
            if length != 0:
                # Используем ранее вычисленное значение префикс-функции
                length = prefix[length - 1]
            else:
                prefix[i] = 0
                i += 1
    
    return prefix


def kmp_search(text, pattern):
    """
    Поиск подстроки в тексте с использованием алгоритма KMP
    
    Возвращает список индексов начала всех вхождений паттерна в текст.
    """
    n = len(text)
    m = len(pattern)
    
    if m == 0 or n < m:
        return []  # пустой паттерн
    
    # Строим префикс-функцию
    prefix = build_prefix_function(pattern)
    print(prefix)
    
    indices = []  # индексы начала вхождений
    i = 0  # индекс для текста
    j = 0  # индекс для паттерна
    
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            
            if j == m:
                # Найдено полное совпадение
                indices.append(i - j)
                # Используем префикс-функцию для поиска следующего возможного вхождения
                j = prefix[j - 1]
        else:
            if j != 0:
                # Используем префикс-функцию для определения следующей позиции в паттерне
                j = prefix[j - 1]
            else:
                # Нет совпадения, двигаемся по тексту
                i += 1
    
    return indices

string = input()
substring = input()
result = kmp_search(string, substring)
print(result)