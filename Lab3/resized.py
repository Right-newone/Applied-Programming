import cv2
import numpy as np
def resizing_img(image: np.ndarray, new_width: int, new_height: int) -> np.ndarray | None:
    """
    Изменяет размер изображения с подбором интерполяции.
    :param image: Исходное изображение.
    :param new_width: Новая ширина изображения.
    :param new_height: Новая высота изображения.
    :return: Изображение с новыми размерами или None при ошибке.
    """
    if new_width <= 0 or new_height <= 0:
        print("Ошибка: размеры должны быть положительными!")
        return None
   
    if new_width < image.shape[1] or new_height < image.shape[0]:
        interpolation = cv2.INTER_AREA
    else:
        interpolation = cv2.INTER_CUBIC

    new_size_img = cv2.resize(image, (new_width, new_height), interpolation=interpolation)
    return new_size_img
