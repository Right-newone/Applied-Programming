import argparse
def get_arguments() -> argparse.Namespace:
    """
    Парсинг аргументов командной строки.
    :return: Объект с аргументами.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--rating", required=True, type=str, help="Рейтинг (Three, Four, Five)")
    parser.add_argument("-d", "--dir", required=True, type=str, help="Путь к папке для сохранения")
    parser.add_argument("-a", "--annotation", required=True, type=str, help="Путь к файлу аннотации")
    return parser.parse_args()