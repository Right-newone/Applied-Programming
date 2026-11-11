import argparse
def get_arguments() -> argparse.Namespace:
    """
    Парсинг аргументов командной строки.
    :return: Объект с аргументами.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, type=str, help="Путь к исходному файлу")
    parser.add_argument("-r", "--result", required=True, type=str, help="Путь к результирующему файлу")
    parser.add_argument("--w", required=True, type=int, help="Ширина изображения")
    parser.add_argument("--h", required=True, type=int, help="Высота изображения")
    return parser.parse_args()