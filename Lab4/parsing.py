import argparse

def parser()-> argparse.Namespace:
    """
    Парсинг аргументов командной строки.
    :return: Объект с аргументами.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--result', required=True, type=str, help='Путь к сохранению результирующего файла')
    parser.add_argument('-rj', '--result_diagram', required=True, type=str, help='Путь к сохранению графика файла')
    return parser.parse_args()
