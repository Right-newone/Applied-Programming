import numpy as np
def start_size_demo(image: np.ndarray) -> None:
    """
    Выводит исходные размеры изображения в консоль.
    :param image: Исходное изображение.
    """
    print(f"Исходные размеры изображения: {image.shape[0], image.shape[1]}")