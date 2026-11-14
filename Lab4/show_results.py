import matplotlib.pyplot as plt
import pandas as pd
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