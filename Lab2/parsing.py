import csv
import os
from typing import Any
from urllib.parse import urljoin
from download import download_cover
BASE_URL = "https://books.toscrape.com/"
HEADERS = {"User-Agent": "Mozilla/5.0"}
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