import cv2
import os

from get_args import get_arguments
from binominized import binomize_img
from resized import resizing_img
from default_img_demo import start_size_demo
from bordered import border
from results_demo import show_results

def main() -> None:
    """
    Основная функция, объединяющая все этапы программы.
    """
    args = get_arguments()
    img_bgr = cv2.imread(args.input)

    if img_bgr is None:
        print("Не удалось загрузить картинку.")
        return
    
    start_size_demo(img_bgr)
    
    binary_img = binomize_img(img_bgr)
    
    resized_img = resizing_img(img_bgr, args.w, args.h)
    if resized_img is None:
        return
        
    bordered_img = border(img_bgr)

    base_name, _ = os.path.splitext(args.result)
    ext = '.jpg'
    
    cv2.imwrite(f"{base_name}_bin{ext}", binary_img)
    cv2.imwrite(f"{base_name}_resized{ext}", resized_img)
    cv2.imwrite(f"{base_name}_bordered{ext}", bordered_img)
    
    show_results(img_bgr, binary_img, resized_img, bordered_img)

if __name__ == '__main__':
    main()