import time
import requests
from bs4 import BeautifulSoup
from iterators import SimpleIterator
from parsing import parsing_img
from urllib.parse import urljoin
BASE_URL = "https://books.toscrape.com/"
HEADERS = {"User-Agent": "Mozilla/5.0"}
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