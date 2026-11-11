import requests
BASE_URL = "https://books.toscrape.com/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

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