import argparse
import csv
import os
import time
from typing import Any
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

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

def create_annotation_header(annotation_file: str) -> None:
    """
    Создает файл аннотации и записывает в него заголовки таблицы.
    :param annotation_file: Путь к файлу аннотации.
    """
    with open(annotation_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Номер", "Название книги", "Имя файла", "Относительный путь", "Абсолютный путь"])

def download_cover(img_url: str, save_path: str) -> bool:
    """
    Скачивает изображение по ссылке и сохраняет его.
    :param img_url: Прямая ссылка на картинку.
    :param save_path: Путь для сохранения файла.
    :return: True, если успешно, иначе False.
    """
    try:
        img_response = requests.get(img_url, headers=HEADERS, timeout=10)
        img_response.raise_for_status()
        with open(save_path, "wb") as file:
            file.write(img_response.content)
        return True
    except requests.exceptions.RequestException as e:
        print(f"Ошибка скачивания картинки: {e}")
        return False

def parsing_img(books: list[Any], user_rate: str, counter_target: int, save_dir: str, annotation_file: str) -> int:
    """
    Ищет обложки по рейтингу, скачивает их и записывает пути в файл аннотации.
    :param books: Список карточек книг на странице.
    :param user_rate: Искомый рейтинг.
    :param counter_target: Текущий счетчик скачанных картинок.
    :param save_dir: Папка для сохранения.
    :param annotation_file: Путь к файлу аннотации.
    :return: Обновленный счетчик скачанных картинок.
    """
    for book in books:
        if counter_target >= 30:
            break

        rating_tag = book.find("p", class_="star-rating")
        if not rating_tag:
            continue

        rating = rating_tag["class"][1]

        if user_rate == rating:
            img_src = book.find("img")["src"]
            title = book.find("img")["alt"]

            full_url = urljoin(BASE_URL, img_src)
            
            file_name = f"book_{counter_target + 1}.jpg"
            path = os.path.join(save_dir, file_name)
            abs_path = os.path.abspath(path)
            rel_path = os.path.relpath(abs_path)

            if download_cover(full_url, path):
                with open(annotation_file, mode='a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f, delimiter=';')
                    writer.writerow([counter_target + 1, title, file_name, rel_path, abs_path])

                counter_target += 1
                print(f"Скачана {counter_target}-я картинка (Рейтинг: {rating})")

    return counter_target

def run_scraper(user_rate: str, save_dir: str, annotation_file: str) -> None:
    """
    Запускает процесс парсинга страниц сайта.
    :param user_rate: Искомый рейтинг.
    :param save_dir: Папка для сохранения.
    :param annotation_file: Путь к файлу аннотации.
    """
    counter_target = 0
    cur_url = BASE_URL

    pages_iterator = SimpleIterator(50)

    for page_num in pages_iterator:
        print(f"\n--- Парсим страницу {page_num} ---")
        try:
            response = requests.get(cur_url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            bs = BeautifulSoup(response.text, "html.parser")
            books = bs.find_all("article", class_="product_pod")
        except requests.exceptions.RequestException as e:
            print(f"Не удалось скачать страницу {page_num}: {e}")
            break

        counter_target = parsing_img(books, user_rate, counter_target, save_dir, annotation_file)

        if counter_target >= 30:
            print(f"\nНабрано {counter_target} обложек.")
            break

        next_tag = bs.find("li", class_="next")
        if next_tag:
            next_href = next_tag.find("a")["href"]
            cur_url = urljoin(cur_url, next_href)
            time.sleep(1)
        else:
            print("Страницы закончились, парсинг завершен.")
            break

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

def main() -> None:
    """
    Основная функция, объединяющая все этапы программы.
    """
    args = get_arguments()
    
    user_rate = args.rating.capitalize()
    save_directory = args.dir
    annotation_file = args.annotation

    os.makedirs(save_directory, exist_ok=True)
    create_annotation_header(annotation_file)

    print(f"Ищем книги с рейтингом: {user_rate}")
    print(f"Сохраняем в папку: {save_directory}")

    run_scraper(user_rate, save_directory, annotation_file)

    test_iterators(save_directory, annotation_file)

if __name__ == "__main__":
    main()