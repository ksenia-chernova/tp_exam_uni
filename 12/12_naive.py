"""
Наивный алгоритм поиска подстроки в строке
"""

def func(string, substring):
    len_string = len(string)
    len_substring = len(substring)
    result = []

    for i in range(len_string - len_substring + 1):
        flag = True
        for j in range(len_substring):
            if string[i + j] != substring[j]:
                flag = False
                break
        if flag:
            result.append(i)

    return result

string = input()
substring = input()
result = func(string, substring)

print(f"string: {string}")
print(f"substring: {substring}")
print(f"result: {result}")