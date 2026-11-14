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
    parser.add_argument('-r', '--result', required=True, type=str, help='Путь к сохранению результирующего файла')
    return parser.parse_args()

def orientation(file_path):
    img = cv2.imread(file_path)
    if img is None:
        return "Ошибка чтения файла"

    if img.shape[1] > img.shape[0]:
        return 'Вертикальное'
    elif img.shape[1] < img.shape[0]:
        return 'Горизонтальное'
    elif img.shape[1] == img.shape[0]:
        return 'Квадратное'

def show(df2):
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.hist(
        df2['Ориентация изображения'],                  
        color='skyblue',
        edgecolor='black',
        label='Количество изображений'
    )

    ax.set_title('Распределение ориентаций изображений')
    ax.set_xlabel('Тип ориентации')
    ax.set_ylabel('Количество изображений')
    ax.legend()
    plt.show()

def main():
    args = parser()
    df = pd.read_csv('annotation.csv', sep=';', encoding='utf-8-sig')
    df2 = df[['Относительный путь', 'Абсолютный путь']]
    df2['Ориентация изображения'] = df2['Абсолютный путь'].apply(orientation)
    df2.to_csv(args.result, sep=';', index=False, encoding='utf-8-sig')
    show(df2)
    
if __name__ == '__main__':
    main()
