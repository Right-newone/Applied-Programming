import pandas as pd
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