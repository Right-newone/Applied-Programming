import argparse
import pandas as pd
import os
import matplotlib.pyplot as plt
import cv2
import numpy as np

def parser()-> argparse.Namespace:
    """
    Парсинг аргументов командной строки.
    :return: Объект с аргументами.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, type=str, help='Путь к исходному файла')
    parser.add_argument('-r', '--result', required=True, type=str, help='Путь к сохранению результирующего файла')
    return parser.parse_args()

def orientation():
    img = cv2.imread('book_11.jpg')
    if img is None:
        print("Ошибка чтения файла")

    if img.shape[0] > img.shape[1]:
        print('Горизонтальное')
    elif img.shape[0] < img.shape[1]:
        print('Вертикальное')
    elif img.shape[0] == img.shape[1]:
        print('Квадратное')

def main():
    args = parser()
    df = pd.read_csv('annotation.csv', sep=';', encoding='utf-8-sig')
    df2 = df[['Относительный путь', 'Абсолютный путь']]
    df['Ориентация изображения'] = df[['Относительный путь', 'Абсолютный путь']].apply(orientation)
    df2.to_csv(args.result, sep=';', index=False, encoding='utf-8-sig')
    
if __name__ == '__main__':
    main()
