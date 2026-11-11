import cv2
import numpy
import argparse


def get_arguments() -> argparse.Namespace:
    """
    Парсинг аргументов командной строки.
    :return: Объект с аргументами.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--size", required=True, type=str, help="Размер изображения, заданный пользователем")
    parser.add_argument("-a", "--result", required=True, type=str, help="Путь к результирующему файлу")
    return parser.parse_args()


path = r"C:\Aplication Programming\Lab3"
img_bgr = cv2.imread("book_11.jpg")
gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

if img_bgr is None:
    raise FileNotFoundError("Не удалось открыть image.jpg")

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
    return new_size_img

def main():
    get_arguments()
    with open("resulting", "wb") as file:
        cv = cv2.imwrite(path, img_bgr)

if __name__ == '__main__':
    main()