import cv2
import numpy as np
import matplotlib.pyplot as plt
def show_results(image: np.ndarray, binary: np.ndarray, resized: np.ndarray, bordered: np.ndarray) -> None:
    """
    Демонстрирует исходное изображение и результаты обработки с помощью Matplotlib.
    :param image: Исходное изображение.
    :param binary: Бинарное изображение.
    :param resized: Изображение с измененным размером.
    :param bordered: Изображение с рамкой.
    """
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    resized_rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    bordered_rgb = cv2.cvtColor(bordered, cv2.COLOR_BGR2RGB)

    fig, ax = plt.subplots(2, 2, figsize=(10, 8))
    
    ax[0, 0].imshow(image_rgb); ax[0, 0].set_title("Исходное"); ax[0, 0].axis("off")
    ax[0, 1].imshow(binary, cmap="gray"); ax[0, 1].set_title("Бинарное"); ax[0, 1].axis("off")
    ax[1, 0].imshow(resized_rgb); ax[1, 0].set_title(f"Ресайз {resized.shape[1]}x{resized.shape[0]}"); ax[1, 0].axis("off")
    ax[1, 1].imshow(bordered_rgb); ax[1, 1].set_title("С рамкой"); ax[1, 1].axis("off")
    
    plt.tight_layout()
    plt.show()