import os
import re
import argparse

directory = r'C:\Applied-Programming\Lab1'
path = os.path.join(directory, 'output.txt')

def parsing():
    """
    Создает парсер аргументов командной строки и добавляет позиционный аргумент.
    
    Проверяет, что введенное пользователем значение является строкой.
    
    :return: Объект Namespace, содержащий введенное имя пользователя (name)
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('name', type=str, help='your name')
    args = parser.parse_args()
    return args


def reading():
    """
    Читает файл data.txt и возвращает его содержимое.
    
    Файл читается построчно. Кодировка файла должна быть UTF-8.
    
    :return: Список строк, прочитанных из файла
    :rtype: list[str]
    """
    with open("data.txt", "r", encoding="utf-8") as file:
        text = file.readlines()
        return text


def creating():
    """
    Создает словарь с подсчетом количества вхождений каждого домена.
    
    Перебирает строки из файла, разбивает их по символу '@', 
    извлекает домен (1-й элемент после разбиения) и увеличивает 
    счетчик для этого домена на единицу.
    
    :return: Словарь, где ключ — имя домена, а значение — количество вхождений
    :rtype: dict[str, int]
    """
    text = reading()
    domen_counts = {}

    for line in text:
        line = line.strip()
        if not line:
            continue
        if '@' not in line:
            continue
        domen = line.split('@')[1]
        domen_counts[domen] = domen_counts.get(domen, 0) + 1
    return domen_counts


def writing():
    """
    Сортирует данные и записывает их в результирующий файл output.txt.
    
    Создает новый файл (режим 'x'). Данные сортируются по убыванию количества.
    Каждый домен проверяется регулярным выражением, и если он валиден, 
    записывается в формате "домен:количество".
    
    :raises FileExistsError: Если файл по указанному пути уже существует (исключение перехватывается внутри функции)
    """
    domen_counts = creating()
    try:
        with open(path, 'x', encoding='utf-8') as file:
            file.write('Домен: количество\n')
            file.write('----------\n')
            
            sorted_domens = sorted(domen_counts.items(), key=lambda x: x[1], reverse=True)
            
            for domen, count in sorted_domens:
                match = re.fullmatch(r"[a-zA-Z0-9._%+-]+\.[a-zA-Z]{2,}", domen)
                if match:
                    file.write(f"{domen}:{count}\n")
                        
    except FileExistsError:
        print(f"Файл уже создан по данному пути: {path}")


def main():
    """
    Главная функция программы.
    
    Выполняет парсинг аргументов, запускает процесс подсчета 
    и записывает результат в файл.
    """
    args = parsing()        
    domen_counts = creating() 
    writing()               


if __name__ == '__main__':
    main()