import argparse
import pandas as pd
import matplotlib.pyplot as plt
import cv2

def parser()-> argparse.Namespace:
    """
    Парсинг аргументов командной строки.
    :return: Объект с аргументами.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--result', required=True, type=str, help='Путь к сохранению результирующего файла')
    parser.add_argument('-rj', '--result_diagram', required=True, type=str, help='Путь к сохранению графика файла')
    return parser.parse_args()

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

def show(df: pd.DataFrame, output_path: str) -> None:
    """
    Строит гистограмму распределения ориентаций и сохраняет её.

    :param df: DataFrame с колонкой 'Ориентация изображения'.
    :type df: pd.DataFrame
    :param output_path: Путь для сохранения файла с графиком.
    :type output_path: str
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    ax.hist(
        df['Ориентация изображения'],                  
        color='skyblue',
        edgecolor='black',
        label='Количество изображений'
    )

    ax.set_title('Распределение ориентаций изображений', fontsize=14)
    ax.set_xlabel('Тип ориентации', fontsize=12)
    ax.set_ylabel('Количество изображений', fontsize=12)
    ax.grid(True, axis='y', linestyle='--', alpha=0.4)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()

def sort_by_orientation(df) -> pd.DataFrame:
    """
    Сортирует DataFrame по колонке 'Ориентация изображения'.
    :param df:        DataFrame с колонкой 'Ориентация изображения'
    :return:          новый отсортированный DataFrame
    """
    return df.sort_values(by='Ориентация изображения', kind='stable').reset_index(drop=True)

def filtered(df: pd.DataFrame, orientation_value: str) -> pd.DataFrame:
    """
    Фильтрует DataFrame по значению ориентации.

    :param df: DataFrame с колонкой 'Ориентация изображения'.
    :type df: pd.DataFrame
    :param orientation_value: Значение для фильтрации.
    :type orientation_value: str
    :return: Отфильтрованный DataFrame.
    :rtype: pd.DataFrame
    """
    return df.query("`Ориентация изображения` == @orientation_value").reset_index(drop=True)

def main()-> None:
    """Основная точка входа в программу."""
    args = parser()
    df = pd.read_csv('annotation.csv', sep=';', encoding='utf-8-sig')
    df2 = df[['Относительный путь', 'Абсолютный путь']].copy()
    df2['Ориентация изображения'] = df2['Абсолютный путь'].apply(orientation)
    df2 = sort_by_orientation(df2)
    
    df2.to_csv(args.result, sep=';', index=False, encoding='utf-8-sig')
    show(df2, args.result_diagram)

    df_horizontal = filtered(df2, 'Горизонтальное')
    df_horizontal.to_csv('horizontal_only.csv', sep=';', index=False, encoding='utf-8-sig')

if __name__ == '__main__':
    main()
