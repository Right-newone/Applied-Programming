from iterators import Iterator

def test_iterators(save_dir: str, annotation_file: str) -> None:
    """
    Демонстрирует работу итератора на папке и на файле аннотации.
    :param save_dir: Путь к папке с картинками.
    :param annotation_file: Путь к файлу аннотации.
    """
    print("\n--- Проверка файлов с помощью итератора ---")
    
    print("\n1. Перебор файлов в папке:")
    file_iterator_dir = Iterator(save_dir)
    for file_path in file_iterator_dir:
        print(f"Найден файл: {file_path}")

    print("\n2. Перебор путей из файла аннотации:")
    file_iterator_csv = Iterator(annotation_file)
    for file_path in file_iterator_csv:
        print(f"Путь из CSV: {file_path}")