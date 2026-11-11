import cv2
import numpy
import argparse
import os
import random

def get_arguments() -> argparse.Namespace:
    """
    Парсинг аргументов командной строки.
    :return: Объект с аргументами.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--result", required=True, type=str, help="Путь к результирующему файлу")
    return parser.parse_args()

def load_random_files(folder_path):
    all_items = os.listdir(folder_path)

    valid_extentions = ('.jpg')

    image_files = [f for f in all_items if f.lower().endswith(valid_extentions)]

    if not image_files:
        raise FileNotFoundError(f"В папке {folder_path} нет изображений")

    random_file = random.choice(image_files)
    result = os.path.join(folder_path, random_file)
    if result:
        print(f"Найден случайный файл {random_file}")

    img = cv2.imread(result)
    return img

def binomize_img(img_bgr, output_path):
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)    
    threshold = 127
    _, binomized = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    if img_bgr is None:
        raise FileNotFoundError("Не удалось открыть файл f:{input_path}")

    path = r"C:\Aplication Programming\Lab3"
    output_filename = "output.jpg"

    output_path = os.path.join(path, output_filename)
    result = cv2.imwrite(output_path, binomized)
    if result:
        print(f"Успешно сохранено в: {output_path}")
    else:
        print("Ошибка при сохранении файла.")

def resizing_img(image):
    try:
        new_height = int(input("Введите значение высоты изображения(>0): "))
        new_width = int(input("Введите значение ширины изображения(>0): "))
    except ValueError:
        print("Ошибка: нужно вводить целые числа!")
        return None

    if new_width <= 0 or new_height <= 0:
        print("Ошибка: размеры должны быть положительными!")
        return None
   
    if new_width < image.shape[1] or new_height < image.shape[0]:
        interpolation = cv2.INTER_AREA
    else:
        interpolation = cv2.INTER_CUBIC

    new_size_img = cv2.resize(image, (new_width, new_height), interpolation = interpolation)

    path = r"C:\Aplication Programming\Lab3"
    output_filename = "output_resized.jpg"
    output_path = os.path.join(path, output_filename)

    result = cv2.imwrite(output_path, new_size_img)
    if result:
        print(f"Успешно сохранено в: {output_path}")
    else:
        print("Ошибка при сохранении файла.")
    
    return new_size_img

def main():
    get_arguments()

    folder_path = r"C:\Aplication Programming\Lab2\covers"
    img_bgr = load_random_files(folder_path)

    if img_bgr is None:
        print("Не удалось загрузить картинку.")
        return
    
    output_bin = r"C:\Aplication Programming\Lab3\output_bin.jpg"
    binomize_img(img_bgr, output_bin)
    
    resizing_img(img_bgr)
    

if __name__ == '__main__':
    main()