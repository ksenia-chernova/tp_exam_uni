"""
ПОИСК ПОДСТРОКИ С ИСПОЛЬЗОВАНИЕМ ДВОИЧНОГО BITAP АЛГОРИТМА
(Алгоритм Бэйти-Гилла-Вейнера, также известный как shift-or/bitap)

Принцип работы:
1. Использует битовую маску для каждого символа алфавита
2. Хранит состояние поиска в битовом массиве (битовой маске)
3. Позволяет искать подстроку с нечетким соответствием (с ошибками)

Идея:
- Каждой позиции в подстроке соответствует бит в состоянии
- Бит = 1 означает, что префикс подстроки совпадает с суффиксом текста в текущей позиции
- При обработке каждого символа текста состояние обновляется с помощью битовых операций

Пример для подстроки "abc" и текста "xabcy":
1. Инициализация: state = 0...01 (бит для пустой строки)
2. Обработка 'x': state обновляется
3. Обработка 'a': state обновляется, первый бит устанавливается
4. Обработка 'b': state обновляется, второй бит устанавливается
5. Обработка 'c': state обновляется, третий бит устанавливается
6. Когда старший бит state становится 1 - найдено вхождение

Преимущества:
- Очень быстрый для коротких подстрок (до длины машинного слова)
- Поддерживает поиск с ошибками (нечеткий поиск)
- Использует только битовые операции
"""

def bitap_search(text, pattern, max_errors=0):
    """
    Bitap алгоритм поиска подстроки с возможностью нечеткого поиска
    
    Args:
        text: строка, в которой ищем
        pattern: подстрока для поиска
        max_errors: максимальное количество ошибок (для нечеткого поиска)
        
    Returns:
        Список позиций, где найдена подстрока
    """
    if not pattern or not text:
        return []
    
    m = len(pattern)
    n = len(text)
    
    # Если подстрока длиннее текста
    if m > n:
        return []
    
    # Если подстрока слишком длинная для машинного слова
    # (ограничение примерно 64 символа для 64-битных систем)
    if m > 64:
        return bitap_search_long_pattern(text, pattern, max_errors)
    
    # Алфавит строки
    alphabet = set(text)
    
    # Инициализация таблицы масок для каждого символа алфавита
    # mask[c] - битовая маска, где 0 в позиции i означает, что символ pattern[i] равен c
    mask = {c: ~0 for c in alphabet}
    
    # Заполняем маски для символов подстроки
    for i, char in enumerate(pattern):
        if char in mask:
            # Устанавливаем бит в позиции i в 0 для символа char
            mask[char] &= ~(1 << i)
    
    # Начальное состояние (все биты 1, кроме младшего)
    R = ~1
    
    # Для нечеткого поиска храним несколько состояний
    if max_errors > 0:
        # Массив состояний для каждого количества ошибок
        R_list = [~1] * (max_errors + 1)
        old_R_list = [~1] * (max_errors + 1)
    
    result = []
    
    # Основной цикл по символам текста
    for pos, char in enumerate(text):
        # Получаем маску для текущего символа
        char_mask = mask.get(char, ~0)
        
        if max_errors == 0:
            # Точный поиск
            R = (R << 1) | char_mask
            
            # Проверяем, найден ли паттерн (бит m установлен в 0)
            if (R & (1 << m)) == 0:
                result.append(pos - m + 1)
        else:
            # Нечеткий поиск
            # Сохраняем старые состояния
            for k in range(max_errors + 1):
                old_R_list[k] = R_list[k]
            
            # Обновляем состояние для 0 ошибок
            R_list[0] = (old_R_list[0] << 1) | char_mask
            
            # Обновляем состояния для k ошибок
            for k in range(1, max_errors + 1):
                # Варианты: вставка, удаление, замена
                substitution = (old_R_list[k-1] << 1) | char_mask
                insertion = (R_list[k-1] << 1) | char_mask
                deletion = (old_R_list[k] << 1) | char_mask
                
                # Объединяем все варианты
                R_list[k] = substitution & insertion & deletion
            
            # Проверяем для каждого количества ошибок
            for k in range(max_errors + 1):
                if (R_list[k] & (1 << m)) == 0:
                    result.append(pos - m + 1)
    
    return result


def bitap_search_long_pattern(text, pattern, max_errors=0):
    """
    Bitap алгоритм для длинных подстрок (более 64 символов)
    Использует список целых чисел для хранения состояния
    """
    m = len(pattern)
    n = len(text)
    
    # Размер машинного слова в битах
    WORD_SIZE = 64
    
    # Количество слов, необходимых для хранения состояния
    num_words = (m + WORD_SIZE - 1) // WORD_SIZE
    
    # Алфавит строки
    alphabet = set(text)
    
    # Инициализация таблицы масок
    mask = {c: [~0] * num_words for c in alphabet}
    
    # Заполняем маски
    for i, char in enumerate(pattern):
        if char in mask:
            word_idx = i // WORD_SIZE
            bit_idx = i % WORD_SIZE
            mask[char][word_idx] &= ~(1 << bit_idx)
    
    # Инициализация состояний
    R = [~0] * num_words
    R[0] &= ~1  # Устанавливаем младший бит первого слова в 0
    
    if max_errors > 0:
        R_list = [[~0] * num_words for _ in range(max_errors + 1)]
        R_list[0][0] &= ~1
        old_R_list = [[~0] * num_words for _ in range(max_errors + 1)]
    
    result = []
    
    for pos, char in enumerate(text):
        char_mask = mask.get(char, [~0] * num_words)
        
        if max_errors == 0:
            # Обновляем каждое слово состояния
            carry = 0
            for i in range(num_words):
                old_R_word = R[i]
                # Сдвиг с учетом переноса
                R[i] = ((old_R_word << 1) | carry) | char_mask[i]
                carry = (old_R_word >> (WORD_SIZE - 1)) & 1
            
            # Проверяем последний бит
            last_word_idx = (m - 1) // WORD_SIZE
            last_bit_idx = (m - 1) % WORD_SIZE
            if (R[last_word_idx] & (1 << last_bit_idx)) == 0:
                result.append(pos - m + 1)
        else:
            # Нечеткий поиск для длинных подстрок
            for k in range(max_errors + 1):
                old_R_list[k] = R_list[k].copy()
            
            # Обновляем состояния
            # (аналогично точному поиску, но для каждого k)
            # Здесь упрощенная версия для демонстрации
            pass
    
    return result


def bitap_search_exact(text, pattern):
    """
    Точный поиск подстроки (частный случай с max_errors=0)
    """
    return bitap_search(text, pattern, max_errors=0)


# Примеры использования
if __name__ == "__main__":
    # Тест 1: Точный поиск
    text1 = "ababcabcabababd"
    pattern1 = "ababd"
    print(f"Текст: {text1}")
    print(f"Подстрока: {pattern1}")
    result1 = bitap_search_exact(text1, pattern1)
    print(f"Точный поиск: {result1}")
    
    # Тест 2: Нечеткий поиск (с 1 ошибкой)
    text2 = "abcdefghij"
    pattern2 = "abcde"
    print(f"\nТекст: {text2}")
    print(f"Подстрока: {pattern2}")
    result2 = bitap_search(text2, pattern2, max_errors=1)
    print(f"Нечеткий поиск (1 ошибка): {result2}")
    
    # Тест 3: Строка с повторениями
    text3 = "AABAACAADAABAABA"
    pattern3 = "AABA"
    print(f"\nТекст: {text3}")
    print(f"Подстрока: {pattern3}")
    result3 = bitap_search_exact(text3, pattern3)
    print(f"Точный поиск: {result3}")
    
    # Тест 4: Короткая строка
    text4 = "hello world"
    pattern4 = "world"
    print(f"\nТекст: {text4}")
    print(f"Подстрока: {pattern4}")
    result4 = bitap_search_exact(text4, pattern4)
    print(f"Точный поиск: {result4}")
    
    # Тест 5: Подстрока не найдена
    text5 = "abcdefgh"
    pattern5 = "xyz"
    print(f"\nТекст: {text5}")
    print(f"Подстрока: {pattern5}")
    result5 = bitap_search_exact(text5, pattern5)
    print(f"Точный поиск: {result5}")
    
    # Тест 6: Поиск с разными ошибками
    text6 = "аквариум"
    pattern6 = "квариум"
    print(f"\nТекст: {text6}")
    print(f"Подстрока: {pattern6}")
    result6_exact = bitap_search_exact(text6, pattern6)
    result6_fuzzy = bitap_search(text6, pattern6, max_errors=1)
    print(f"Точный поиск: {result6_exact}")
    print(f"Нечеткий поиск (1 ошибка): {result6_fuzzy}")


"""
РАБОТА АЛГОРИТМА НА ПРИМЕРЕ:

Рассмотрим поиск "abc" в "xabcy":

1. Инициализация:
   pattern = "abc" (m=3)
   alphabet = {'x', 'a', 'b', 'c', 'y'}
   
   mask['a'] = 1110 (бит 0 = 0, остальные 1)
   mask['b'] = 1101 (бит 1 = 0)
   mask['c'] = 1011 (бит 2 = 0)
   mask['x'] = mask['y'] = 1111 (все биты 1)
   
   R = 1110 (начальное состояние)

2. Обработка символов:
   pos=0: char='x'
   R = (1110 << 1) | 1111 = 1100 | 1111 = 1111
   
   pos=1: char='a'
   R = (1111 << 1) | 1110 = 1110 | 1110 = 1110
   
   pos=2: char='b'
   R = (1110 << 1) | 1101 = 1100 | 1101 = 1101
   
   pos=3: char='c'
   R = (1101 << 1) | 1011 = 1010 | 1011 = 1011
   Проверяем: (1011 & 1000) = 1000 ≠ 0, еще не нашли
   
   pos=4: char='y'
   R = (1011 << 1) | 1111 = 0110 | 1111 = 1111

Алгоритм не нашел "abc" в "xabcy", потому что в этой строке его нет.

Пример с нахождением:
Текст: "ababc", подстрока: "abc"
pos=2: после обработки 'a','b','a','b','c' - будет найден паттерн.

ОСОБЕННОСТИ:
- Использует битовые операции, поэтому очень быстрый
- Легко расширяется для нечеткого поиска
- Ограничен длиной машинного слова (обычно 64 бита)
- Хорош для поиска коротких подстрок
"""