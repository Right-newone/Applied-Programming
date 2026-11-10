import cv2
import numpy

path = r"C:\Aplication Programming\Lab3"
img_bgr = cv2.imread("book_11.jpg")
gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
if img_bgr is None:
    raise FileNotFoundError("Не удалось открыть image.jpg")
def main():
    with open("result", "wb") as file:
        cv = cv2.imwrite(path, img_bgr)

if __name__ == '__main__':
    main()