from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import os
import time 
import argparse

base_url = "https://books.toscrape.com/"
headers = {"User-Agent": "Mozilla/5.0"}      

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
            
            from urllib.parse import urljoin
            full_url = urljoin(base_url, img_src)
            
            try:
                img_response = requests.get(full_url, headers=headers, timeout=10)
                img_response.raise_for_status()

                file_name = f"book_{counter_target + 1}.jpg"
                path = os.path.join(save_dir, file_name)
      
                with open(path, "wb") as file:
                    file.write(img_response.content)
                
                # Записываем в аннотацию (режим 'a' - добавление)
                with open(annotation_file, 'a', encoding='utf-8') as f:
                    f.write(f"{counter_target + 1}. {title} | Файл: {file_name}\n")

                counter_target += 1
                print(f"Скачана {counter_target}-я картинка (Рейтинг: {rating})")
      
            except requests.exceptions.RequestException as e:
                print(f"Ошибка скачивания картинки: {e}")
                continue 
                
    return counter_target

def main():
    parser = argparse.ArgumentParser(description="Скачивание обложек книг по рейтингу.")
    parser.add_argument("-r", "--rating", required=True, type=str, help="Рейтинг (Three, Four, Five)")
    parser.add_argument("-d", "--dir", required=True, type=str, help="Путь к папке для сохранения")
    parser.add_argument("-a", "--annotation", required=True, type=str, help="Путь к файлу аннотации")
    
    args = parser.parse_args()
    
    user_rate = args.rating.capitalize()
    save_directory = args.dir
    annotation_file = args.annotation

    os.makedirs(save_directory, exist_ok=True)

    with open(annotation_file, 'w', encoding='utf-8') as f:
        f.write(f"--- Список книг с рейтингом {user_rate} ---\n")

    pagenum = 1
    counter_target = 0
    cur_url = base_url

    print(f"Ищем книги с рейтингом: {user_rate}")
    print(f"Сохраняем в папку: {save_directory}")

    while pagenum <= 50 and counter_target < 30:
        print(f"\n--- Парсим страницу {pagenum} ---")
        try:
            response = requests.get(cur_url, headers=headers, timeout=10)
            response.raise_for_status()
            bs = BeautifulSoup(response.text, "html.parser")
            books = bs.find_all("article", class_="product_pod")
        except requests.exceptions.RequestException as e:
            print(f"Не удалось скачать страницу {pagenum}: {e}")
            break

        counter_target = parsing_img(books, user_rate, counter_target, save_directory, annotation_file)
        
        if counter_target >= 30:
            print(f"\nНабрано {counter_target} обложек.")
            break

        next_tag = bs.find("li", class_="next")
        if next_tag:
            next_href = next_tag.find("a")["href"]

            cur_url = urljoin(cur_url, next_href)
            pagenum += 1
            time.sleep(1) 
        else:
            print("Страницы закончились, парсинг завершен.")
            break

if __name__ == '__main__':
    main()