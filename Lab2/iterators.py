import csv
import os
class SimpleIterator:
    """
    Итератор для генерации номеров страниц.
    """
    def __init__(self, limit: int) -> None:
        """
        Инициализация итератора.
        :param limit: Максимальное количество страниц.
        """
        self.limit = limit
        self.counter = 0

    def __iter__(self) -> 'SimpleIterator':
        """Возвращает самого себя."""
        return self

    def __next__(self) -> int:
        """Возвращает следующее число, пока не достигнут лимит."""
        if self.counter < self.limit:
            self.counter += 1
            return self.counter
        else:
            raise StopIteration

class Iterator:
    """
    Итератор для перебора путей к файлам из папки или CSV-файла.
    """
    def __init__(self, source: str) -> None:
        """
        Инициализация итератора путей.
        :param source: Путь к папке или к файлу аннотации.
        """
        self.paths: list[str] = []
        self.index: int = 0

        if os.path.isdir(source):
            print(f"Источник: папка {source}")
            for filename in os.listdir(source):
                full_path = os.path.join(source, filename)
                if os.path.isfile(full_path):
                    self.paths.append(full_path)

        elif os.path.isfile(source):
            print(f"Источник: файл {source}")
            with open(source, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')
                for row in reader:
                    if not row or "---" in row[0] or row[0] == "Номер":
                        continue
                    absolute_path = row[-1]
                    self.paths.append(absolute_path)

    def __iter__(self) -> 'Iterator':
        """Возвращает самого себя."""
        return self

    def __next__(self) -> str:
        """Возвращает следующий путь к файлу."""
        if self.index < len(self.paths):
            path = self.paths[self.index]
            self.index += 1
            return path
        else:
            raise StopIteration