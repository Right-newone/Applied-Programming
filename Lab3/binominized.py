import cv2
import numpy as np

def binomize_img(img_bgr: np.ndarray) -> np.ndarray:
    """
    Преобразует цветное изображение в бинарное (черно-белое).
    :param img_bgr: Исходное изображение в формате BGR.
    :return: Бинарное изображение.
    """
    if img_bgr is None:
        raise FileNotFoundError(f"Не удалось открыть файл")
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)    
    threshold = 127
    _, binomized = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return binomized