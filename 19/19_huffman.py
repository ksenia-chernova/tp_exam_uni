"""
СТАТИЧЕСКОЕ СЖАТИЕ БЕЗ ПОТЕРЬ - КОДИРОВАНИЕ ХАФФМАНА

Принцип работы:
1. Подсчет частот символов в исходном тексте
2. Построение дерева Хаффмана (бинарное дерево)
3. Назначение кодов символам: более частые символы получают более короткие коды
4. Кодирование текста с использованием полученных кодов

Пример:
Текст: "abracadabra"

Частоты:
a: 5, b: 2, r: 2, c: 1, d: 1

Построение дерева:
1. c(1) + d(1) = 2
2. b(2) + r(2) = 4
3. (c+d)(2) + a(5) = 7
4. (b+r)(4) + (c+d+a)(7) = 11

Коды:
a: 0
b: 10
r: 11
c: 100
d: 101

Закодированный текст: 0 10 11 0 100 0 101 0 11 0
"""

import heapq
from collections import Counter, defaultdict
from typing import Dict, Tuple, Optional


class HuffmanNode:
    """Узел дерева Хаффмана"""
    def __init__(self, char: Optional[str], freq: int):
        self.char = char  # Символ (None для внутренних узлов)
        self.freq = freq  # Частота
        self.left: Optional[HuffmanNode] = None
        self.right: Optional[HuffmanNode] = None
    
    def __lt__(self, other: 'HuffmanNode') -> bool:
        # Для работы с heapq
        return self.freq < other.freq
    
    def __repr__(self) -> str:
        return f"HuffmanNode(char={self.char}, freq={self.freq})"


class StaticHuffmanCoder:
    """Статическое кодирование Хаффмана"""
    
    def __init__(self):
        self.codes: Dict[str, str] = {}  # Коды Хаффмана для символов
        self.reverse_codes: Dict[str, str] = {}  # Обратное отображение код->символ
    
    def build_frequency_table(self, text: str) -> Dict[str, int]:
        """Построение таблицы частот символов"""
        return dict(Counter(text))
    
    def build_huffman_tree(self, freq_table: Dict[str, int]) -> Optional[HuffmanNode]:
        """Построение дерева Хаффмана"""
        if not freq_table:
            return None
        
        # Создаем узлы для каждого символа
        heap = []
        for char, freq in freq_table.items():
            node = HuffmanNode(char, freq)
            heapq.heappush(heap, node)
        
        # Строим дерево
        while len(heap) > 1:
            # Берем два узла с наименьшей частотой
            node1 = heapq.heappop(heap)
            node2 = heapq.heappop(heap)
            
            # Создаем новый внутренний узел
            merged = HuffmanNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            
            heapq.heappush(heap, merged)
        
        return heap[0] if heap else None
    
    def generate_codes(self, node: Optional[HuffmanNode], code: str = "") -> None:
        """Рекурсивная генерация кодов Хаффмана"""
        if node is None:
            return
        
        # Если это листовой узел (символ)
        if node.char is not None:
            self.codes[node.char] = code
            self.reverse_codes[code] = node.char
            return
        
        # Рекурсивно обходим левое и правое поддеревья
        self.generate_codes(node.left, code + "0")
        self.generate_codes(node.right, code + "1")
    
    def print_tree(self, node: Optional[HuffmanNode], indent: str = "", is_last: bool = True) -> None:
        """Визуализация дерева Хаффмана"""
        if node is None:
            return
        
        print(f"{indent}{'└── ' if is_last else '├── '}", end="")
        
        if node.char is not None:
            print(f"'{node.char}' (freq={node.freq}, code={self.codes.get(node.char, '')})")
        else:
            print(f"* (freq={node.freq})")
        
        indent += "    " if is_last else "│   "
        
        # Обходим детей
        if node.left:
            self.print_tree(node.left, indent, False)
        if node.right:
            self.print_tree(node.right, indent, True)
    
    def encode(self, text: str) -> Tuple[str, Dict[str, int]]:
        """Кодирование текста"""
        if not text:
            return "", {}
        
        # 1. Подсчет частот
        freq_table = self.build_frequency_table(text)
        print("Таблица частот:")
        for char, freq in sorted(freq_table.items()):
            print(f"  '{char}': {freq}")
        print()
        
        # 2. Построение дерева
        root = self.build_huffman_tree(freq_table)
        
        # 3. Генерация кодов
        self.codes = {}
        self.reverse_codes = {}
        self.generate_codes(root)
        
        print("Коды Хаффмана:")
        for char, code in sorted(self.codes.items()):
            print(f"  '{char}': {code}")
        print()
        
        # 4. Кодирование текста
        encoded_bits = ""
        for char in text:
            encoded_bits += self.codes[char]
        
        print("Визуализация дерева Хаффмана:")
        self.print_tree(root)
        print()
        
        return encoded_bits, freq_table
    
    def decode(self, encoded_bits: str, freq_table: Dict[str, int]) -> str:
        """Декодирование битовой строки"""
        if not encoded_bits or not freq_table:
            return ""
        
        # Восстанавливаем дерево (если коды не были сохранены)
        if not self.codes:
            root = self.build_huffman_tree(freq_table)
            self.codes = {}
            self.reverse_codes = {}
            self.generate_codes(root)
        
        # Декодирование
        decoded_text = ""
        current_code = ""
        
        for bit in encoded_bits:
            current_code += bit
            if current_code in self.reverse_codes:
                decoded_text += self.reverse_codes[current_code]
                current_code = ""
        
        return decoded_text


def calculate_compression_ratio(original_text: str, encoded_bits: str) -> None:
    """Вычисление степени сжатия"""
    original_size = len(original_text) * 8  # В битах (предполагаем ASCII)
    compressed_size = len(encoded_bits)
    
    ratio = compressed_size / original_size if original_size > 0 else 0
    percentage = (1 - ratio) * 100
    
    print(f"\nАнализ сжатия:")
    print(f"  Размер оригинала: {original_size} бит ({len(original_text)} байт)")
    print(f"  Размер сжатого: {compressed_size} бит ({compressed_size / 8:.2f} байт)")
    print(f"  Степень сжатия: {ratio:.2%}")
    print(f"  Экономия: {percentage:.1f}%")


def huffman_adaptive_demo():
    """Демонстрация адаптивного кодирования Хаффмана"""
    print("="*60)
    print("АДАПТИВНОЕ КОДИРОВАНИЕ ХАФФМАНА (ДЕМО)")
    print("="*60)
    
    # Пример текста с разным распределением символов
    test_cases = [
        ("abracadabra", "Текст с повторяющимися символами"),
        ("hello world", "Текст с пробелами"),
        ("aaaaaaaaaa", "Текст с одним символом"),
        ("abcdefghij", "Текст со всеми разными символами"),
        ("Mississippi", "Текст с разным регистром"),
    ]
    
    for text, description in test_cases:
        print(f"\n{description}: '{text}'")
        print("-"*40)
        
        coder = StaticHuffmanCoder()
        encoded, freq_table = coder.encode(text)
        
        print(f"Закодированная строка: {encoded}")
        
        decoded = coder.decode(encoded, freq_table)
        print(f"Декодированная строка: '{decoded}'")
        print(f"Корректность: {text == decoded}")
        
        calculate_compression_ratio(text, encoded)


def huffman_with_header():
    """Кодирование с сохранением заголовка (частотной таблицы)"""
    print("="*60)
    print("КОДИРОВАНИЕ С ЗАГОЛОВКОМ")
    print("="*60)
    
    text = "to be or not to be"
    print(f"Исходный текст: '{text}'")
    
    # Кодирование
    coder = StaticHuffmanCoder()
    encoded_bits, freq_table = coder.encode(text)
    
    # Создание заголовка (частотная таблица в бинарном виде)
    # В реальном приложении заголовок сериализуется
    print(f"\nЗаголовок (частотная таблица): {freq_table}")
    
    # Сохранение в файл (демонстрация)
    total_size = len(encoded_bits)
    header_info = f"HEADER:{len(freq_table)}:"
    
    print(f"\nСтруктура сжатого файла:")
    print(f"  1. Заголовок: {header_info}...")
    print(f"  2. Частотная таблица")
    print(f"  3. Закодированные данные: {total_size} бит")
    
    # Декодирование
    decoded = coder.decode(encoded_bits, freq_table)
    print(f"\nДекодированный текст: '{decoded}'")


def huffman_file_compression_demo():
    """Демонстрация сжатия файла"""
    print("="*60)
    print("СЖАТИЕ ФАЙЛА (ДЕМО)")
    print("="*60)
    
    # Имитация файла
    file_content = """This is a sample text file for Huffman compression demonstration.
The quick brown fox jumps over the lazy dog.
Huffman coding is a popular algorithm for lossless data compression.
It is used in many applications like ZIP, GZIP, and image compression."""
    
    print(f"Содержимое файла:\n{file_content[:100]}...\n")
    
    # Кодирование
    coder = StaticHuffmanCoder()
    encoded_bits, freq_table = coder.encode(file_content)
    
    print(f"Исходный размер: {len(file_content)} символов")
    print(f"Размер в битах (ASCII): {len(file_content) * 8}")
    print(f"Закодированный размер: {len(encoded_bits)} бит")
    
    original_bits = len(file_content) * 8
    compressed_bits = len(encoded_bits)
    ratio = compressed_bits / original_bits
    
    print(f"\nСтепень сжатия: {ratio:.2%}")
    print(f"Экономия: {(1 - ratio)*100:.1f}%")
    
    # Декодирование
    decoded = coder.decode(encoded_bits, freq_table)
    print(f"\nКорректность декодирования: {file_content == decoded}")


# Основная программа
if __name__ == "__main__":
    print("="*60)
    print("СТАТИЧЕСКОЕ КОДИРОВАНИЕ ХАФФМАНА")
    print("="*60)
    
    # Пример 1: Простой пример
    print("\nПРИМЕР 1: Кодирование 'abracadabra'")
    print("-"*40)
    
    text1 = "abracadabra"
    coder1 = StaticHuffmanCoder()
    
    print(f"Исходный текст: '{text1}'")
    encoded1, freq1 = coder1.encode(text1)
    print(f"Закодированный текст: {encoded1}")
    
    decoded1 = coder1.decode(encoded1, freq1)
    print(f"Декодированный текст: '{decoded1}'")
    print(f"Корректность: {text1 == decoded1}")
    
    calculate_compression_ratio(text1, encoded1)
    
    # Пример 2: Более сложный текст
    print("\n" + "="*60)
    print("ПРИМЕР 2: Кодирование предложения")
    print("-"*40)
    
    text2 = "the cat sat on the mat"
    coder2 = StaticHuffmanCoder()
    
    print(f"Исходный текст: '{text2}'")
    encoded2, freq2 = coder2.encode(text2)
    print(f"Закодированный текст: {encoded2}")
    
    # Подсчет средней длины кода
    total_chars = len(text2)
    total_bits = len(encoded2)
    avg_code_length = total_bits / total_chars if total_chars > 0 else 0
    
    print(f"\nСредняя длина кода: {avg_code_length:.2f} бит/символ")
    print(f"Теоретический предел (энтропия Шеннона): ~{avg_code_length:.2f} бит/символ")
    
    # Пример 3: Демонстрация с разными текстами
    huffman_adaptive_demo()
    
    # Пример 4: Кодирование с заголовком
    huffman_with_header()
    
    # Пример 5: Сжатие файла
    huffman_file_compression_demo()
    
    # Пример 6: Интерактивный режим
    print("\n" + "="*60)
    print("ИНТЕРАКТИВНЫЙ РЕЖИМ")
    print("="*60)
    
    while True:
        try:
            user_input = input("\nВведите текст для кодирования (или 'exit' для выхода): ")
            if user_input.lower() == 'exit':
                break
            
            if not user_input:
                print("Введена пустая строка")
                continue
            
            coder = StaticHuffmanCoder()
            encoded, freq = coder.encode(user_input)
            
            print(f"\nЗакодированный текст ({len(encoded)} бит):")
            # Выводим сгруппированно по 8 бит для удобства
            for i in range(0, len(encoded), 8):
                print(encoded[i:i+8], end=" ")
            print()
            
            decoded = coder.decode(encoded, freq)
            print(f"Декодированный текст: '{decoded}'")
            print(f"Корректность: {user_input == decoded}")
            
            calculate_compression_ratio(user_input, encoded)
            
        except KeyboardInterrupt:
            print("\n\nПрограмма завершена.")
            break
        except Exception as e:
            print(f"Ошибка: {e}")


"""
ОСОБЕННОСТИ СТАТИЧЕСКОГО КОДИРОВАНИЯ ХАФФМАНА:

1. ПРЕИМУЩЕСТВА:
   - Оптимальные коды для заданного распределения частот
   - Простота реализации
   - Широко используется в комбинации с другими алгоритмами (DEFLATE в ZIP)

2. НЕДОСТАТКИ:
   - Нужно передавать таблицу частот вместе с данными (заголовок)
   - Не адаптируется к изменению статистики в потоке данных
   - Для небольших текстов заголовок может быть больше самих данных

3. ОБЛАСТИ ПРИМЕНЕНИЯ:
   - Сжатие файлов (ZIP, GZIP, BZIP2)
   - Сжатие изображений (JPEG, PNG)
   - Передача данных
   - Базы данных

4. АЛЬТЕРНАТИВЫ:
   - Адаптивный Хаффман (не требует передачи таблицы)
   - Арифметическое кодирование (более эффективное)
   - LZ-семейство алгоритмов (LZ77, LZ78, LZW)

РАБОТА АЛГОРИТМА ПО ШАГАМ:

1. АНАЛИЗ: Подсчет частот символов в тексте
2. ПОСТРОЕНИЕ ДЕРЕВА:
   - Каждый символ - лист дерева с весом = частоте
   - Повторно объединяем два узла с наименьшим весом
   - Пока не останется один корневой узел
3. ГЕНЕРАЦИЯ КОДОВ:
   - Левая ветвь = 0, правая = 1
   - Код символа = путь от корня к листу
4. КОДИРОВАНИЕ: Замена каждого символа его кодом
5. ДЕКОДИРОВАНИЕ: Проход по дереву согласно битам

ПРИМЕР ДЛЯ "ABRACADABRA":

Частоты: A=5, B=2, R=2, C=1, D=1

Дерево:
        (11)
       /    \
    (5)     (6)
     A     /   \
         (2)   (4)
         C D   / \
             (2) (2)
             B   R

Коды: A=0, B=10, R=11, C=100, D=101

Текст: A B R A C A D A B R A
Коды:  0 10 11 0 100 0 101 0 10 11 0
"""