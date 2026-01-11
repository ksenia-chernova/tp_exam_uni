"""
Сортировка двоичным деревом (Tree Sort)
Исходный массив: [45, 67, 12, 23, 9, 101, 23, 13, 72, 87]

Принцип работы:
1. Строим бинарное дерево поиска из элементов массива
2. Выполняем обход дерева "в порядке возрастания" (in-order traversal)
3. Получаем отсортированные элементы

Пример для массива [45, 67, 12, 23, 9, 101, 23, 13, 72, 87]:

Построение дерева:
       45
      /  \
     12   67
    / \   / \
   9  23 23  101
      \     /
      13   72
            \
             87

Обход "в порядке возрастания":
9 → 12 → 13 → 23 → 23 → 45 → 67 → 72 → 87 → 101
"""

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None # Левый потомок (меньшие значения)
        self.right = None # Правый потомок (большие значения)

def insert_node(root, value):
    """
    Вставка нового значения в бинарное дерево поиска
    """
    if root is None:
        return TreeNode(value)
    
    if value < root.value:
        root.left = insert_node(root.left, value)
    else:
        # Включаем равные значения в правую ветвь
        root.right = insert_node(root.right, value)

    return root

def in_order_traversal(root, result):
    """
    Обход дерева "в порядке возрастания" (in-order traversal)
    """
    if root is not None:
        # 1. Посещаем левое поддерево
        in_order_traversal(root.left, result)
        # 2. Посещаем корень
        result.append(root.value)
        # 3. Посещаем правое поддерево
        in_order_traversal(root.right, result)

def tree_sort(arr):
    """
    Основная функция сортировки двоичным деревом
    """

    # Строим бинарное дерево поиска
    root = None
    for value in arr:
        root = insert_node(root, value)

    # Выполняем обход дерева для получения отсортированного массива
    result = []
    in_order_traversal(root, result)

    return result

array = [45, 67, 12, 23, 9, 101, 23, 13, 72, 87]
print(array)
sorted_array = tree_sort(array)
print(sorted_array)