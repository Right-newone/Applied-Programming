import os
import re
import argparse

directory='C:\\Aplication Programming\\Lab1'
path = os.path.join(directory, 'output.txt')

def parsing():
    #Создается парсер и добавляется позиционный аргумент.
    #Проверка того, что вводит пользователь, если не
    #удовлетворяет условию type=str, то будет ошибка,
    #как и если не вводить имени
    parser=argparse.ArgumentParser()
    parser.add_argument('name', type=str, help='your name')
    args=parser.parse_args()
    return args

def reading():
    #Читается файл и записывается построчно в переменную text
    with open("data.txt", "r", encoding="utf-8") as file:
        text=file.readlines()
        return text

def creating():
    #Создается словарь. Перебираются циклом все строки из файла
    #и разбиваются по символу '\n', после чего отделяется 0 элемент(имя пользователя)
    #и 1 элемент(домен),с помощью разбиения на список строк,
    #но уже по символу '@' и 1 элементы остаются в качестве домена.
    #Далее происходит доступ к значению по ключу, если его нет, возвращается 0,
    #и увеличивается счечик на единицу
    text=reading()
    domen_counts={}

    for line in text:
        line=line.strip()
        if not line:
            continue
        if '@' not in line:
            continue
        domen=line.split('@')[1]
        domen_counts[domen]=domen_counts.get(domen, 0) + 1
    return domen_counts

def writing():
    #Передается в чтение файла путь, по которому будет создаваться
    #результирующий файл, 'x' создает новый файл, если его не было, благодаря исключениям
    #если уже существует файл output.txt, то данные в нем не перезапишутся,
    #а нового файла не добавиться. 
    #Затем сортируется словарь по [1] элементу в порядке убывания числа пользователей
    #с такими доменами. 
    #После чего в цикле, проходящему по уже отсортированному массиву
    #проверяются все домены по шаблону с помощью функции fullmatch()
    #и если они прошли проверку, то печатаются в файл с помощью формат строки
    #в виде {домен}:{число людей} #
    domen_counts=creating()
    try:
        with open(path, 'x', encoding='utf-8') as file:
            file.write('Домен: количество\n')
            file.write('----------\n')
            sorted_domens=sorted(domen_counts.items(), key=lambda x: x[1], reverse=True)
            for domen, count in sorted_domens:
                match=re.fullmatch(r"[a-zA-Z0-9._%+-]+\.[a-zA-Z]{2,}", domen)
                if match:
                    file.write(f"{domen}:{count}\n")
                        
    except FileExistsError:
        print(f"Файл уже создан по данному пути: {path}")

def main():
    #Здесь происходит вызов всех функций и сборка модулей#
    args=parsing()
    reading()
    domen_counts=creating()
    writing()

if __name__ == '__main__':
    main()