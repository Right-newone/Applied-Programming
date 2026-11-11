import csv
def create_annotation_header(annotation_file: str) -> None:
    """
    Создает файл аннотации и записывает в него заголовки таблицы.
    :param annotation_file: Путь к файлу аннотации.
    """
    with open(annotation_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Номер", "Название книги", "Имя файла", "Относительный путь", "Абсолютный путь"])