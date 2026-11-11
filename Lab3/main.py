import cv2
import argparse
import os
import matplotlib.pyplot as plt

def get_arguments() -> argparse.Namespace:
    """
    Парсинг аргументов командной строки.
    :return: Объект с аргументами.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, type=str, help="Путь к исходному файлу")
    parser.add_argument("-r", "--result", required=True, type=str, help="Путь к результирующему файлу")
    parser.add_argument("--w", required=True, type=int, help="Ширина изображения")
    parser.add_argument("--h", required=True, type=int, help="Высота изображения")
    return parser.parse_args()

def binomize_img(img_bgr):
    if img_bgr is None:
        raise FileNotFoundError(f"Не удалось открыть файл {img_bgr}")
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)    
    threshold = 127
    _, binomized = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return binomized

def resizing_img(image, new_width, new_height):
    if new_width <= 0 or new_height <= 0:
        print("Ошибка: размеры должны быть положительными!")
        return None
   
    if new_width < image.shape[1] or new_height < image.shape[0]:
        interpolation = cv2.INTER_AREA
    else:
        interpolation = cv2.INTER_CUBIC

    new_size_img = cv2.resize(image, (new_width, new_height), interpolation = interpolation)
    return new_size_img

def start_size_demo(image):
    print(f"Исходные размеры изображения: {image.shape[0], image.shape[1]}")

def border(image):
    bordered = cv2.copyMakeBorder(image, top = 15, bottom = 15, left = 15, right = 15, borderType=cv2.BORDER_CONSTANT, value = (127, 255, 127))
    return bordered

def show_results(image, binary, resized, bordered):
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

def main():
    args = get_arguments()
    img_bgr = cv2.imread(args.input)

    if img_bgr is None:
        print("Не удалось загрузить картинку.")
        return
    
    start_size_demo(img_bgr)
    binary_img = binomize_img(img_bgr)
    resized_img = resizing_img(img_bgr, args.w, args.h)
    bordered_img = border(img_bgr)

    base_name, ext = os.path.splitext(args.result)
    if not ext:
        ext = '.jpg'
    cv2.imwrite(f"{base_name}_bin{ext}", binary_img)
    cv2.imwrite(f"{base_name}_resized{ext}", resized_img)
    cv2.imwrite(f"{base_name}_bordered{ext}", bordered_img)
    show_results(img_bgr, binary_img, resized_img, bordered_img)

if __name__ == '__main__':
    main()