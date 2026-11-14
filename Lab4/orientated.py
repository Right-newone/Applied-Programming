import cv2

def orientation(file_path: str) -> str:
    """
    Определяет ориентацию изображения по его абсолютному пути.

    :param file_path: Абсолютный путь к файлу изображения.
    :type file_path: str
    :return: Строка с типом ориентации.
    :rtype: str
    """
    img = cv2.imread(file_path)
    if img is None:
        return "Ошибка чтения файла"
    
    print(f"{file_path} -> Ширина: {img.shape[1]}, Высота: {img.shape[0]}")

    if img.shape[1] > img.shape[0]:
        return 'Горизонтальное'
    elif img.shape[1] < img.shape[0]:
        return 'Вертикальное'
    elif img.shape[1] == img.shape[0]:
        return 'Квадратное'
