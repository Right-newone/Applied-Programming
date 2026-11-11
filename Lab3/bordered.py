import cv2
import numpy as np
def border(image: np.ndarray) -> np.ndarray:
    """
    Накладывает цветную рамку вокруг изображения.
    :param image: Исходное изображение.
    :return: Изображение с рамкой.
    """
    bordered = cv2.copyMakeBorder(
        image, top=15, bottom=15, left=15, right=15, 
        borderType=cv2.BORDER_CONSTANT, value=(127, 255, 127)
    )
    return bordered
