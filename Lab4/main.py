import pandas as pd
from parsing import parser
from orientated import orientation
from show_results import show
from sorted_orientation import sort_by_orientation
from filtered_df import filtered

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
