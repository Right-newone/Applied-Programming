from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import os
import time 
import argparse
import csv

base_url = "https://books.toscrape.com/"
headers = {"User-Agent": "Mozilla/5.0"}      

class SimpleIterator:
    def __init__(self, limit):
        self.limit = limit  # ограничение
        self.counter = 0  # счётчик

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter < self.limit:
            self.counter += 1
            return self.counter
        else:
            raise StopIteration

class Iterator:
    def __init__(self, source):
        self.paths = []
        self.index = 0

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

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.paths):
            path = self.paths[self.index]
            self.index += 1
            return path
        else:
            raise StopIteration

def parsing_img(books, user_rate, counter_target, save_dir, annotation_file):
    """
    Ищет обложки по рейтингу, скачивает их и записывает названия в файл аннотации.
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

            full_url = urljoin(base_url, img_src)
            
            try:
                img_response = requests.get(full_url, headers=headers, timeout=10)
                img_response.raise_for_status()

                file_name = f"book_{counter_target + 1}.jpg"
                path = os.path.join(save_dir, file_name)

                abs_path = os.path.abspath(path)
                rel_path = os.path.relpath(abs_path)

                with open(path, "wb") as file:
                    file.write(img_response.content)
                
                with open(annotation_file, mode='a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f, delimiter = ';')
                    writer.writerow([counter_target + 1, title, file_name, rel_path, path])

                counter_target += 1
                print(f"Скачана {counter_target}-я картинка (Рейтинг: {rating})")
      
            except requests.exceptions.RequestException as e:
                print(f"Ошибка скачивания картинки: {e}")
                continue 
                
    return counter_target

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--rating", required=True, type=str, help="Рейтинг (Three, Four, Five)")
    parser.add_argument("-d", "--dir", required=True, type=str, help="Путь к папке для сохранения")
    parser.add_argument("-a", "--annotation", required=True, type=str, help="Путь к файлу аннотации")
    
    args = parser.parse_args()
    
    user_rate = args.rating.capitalize()
    save_directory = args.dir
    annotation_file = args.annotation

    os.makedirs(save_directory, exist_ok=True)

    with open(annotation_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter = ';')
        writer.writerow(["Номер", "Название книги", "Имя файла", "Относительный путь", "Абсолютный путь"])

    counter_target = 0
    cur_url = base_url

    print(f"Ищем книги с рейтингом: {user_rate}")
    print(f"Сохраняем в папку: {save_directory}")

    pages_iterator = SimpleIterator(50)
    
    for page_num in pages_iterator:
        print(f"\n--- Парсим страницу {page_num} ---")
        try:
            response = requests.get(cur_url, headers=headers, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8' 
            bs = BeautifulSoup(response.text, "html.parser")
            books = bs.find_all("article", class_="product_pod")
        except requests.exceptions.RequestException as e:
            print(f"Не удалось скачать страницу {page_num}: {e}")
            break

        counter_target = parsing_img(books, user_rate, counter_target, save_directory, annotation_file)
            
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

    print("\nПеребор файлов в папке:")
    file_iterator_dir = Iterator(save_directory) 
    for file_path in file_iterator_dir:
        print(f"Найден файл: {file_path}")

    print("\nПеребор путей из файла аннотации:")
    file_iterator_csv = Iterator(save_directory) 
    for file_path in file_iterator_csv:
        print(f"Путь из CSV: {file_path}")

if __name__ == '__main__':
    main()