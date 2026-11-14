import pandas as pd
def sort_by_orientation(df) -> pd.DataFrame:
    """
    Сортирует DataFrame по колонке 'Ориентация изображения'.
    :param df:        DataFrame с колонкой 'Ориентация изображения'
    :return:          новый отсортированный DataFrame
    """
    return df.sort_values(by='Ориентация изображения', kind='stable').reset_index(drop=True)