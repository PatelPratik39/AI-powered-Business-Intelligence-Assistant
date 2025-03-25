# utils/visualization_utils.py

import matplotlib.pyplot as plt
import seaborn as sns

def plot_trends(df, column_x, column_y, title):
    """Plot a simple trend line."""
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x=column_x, y=column_y)
    plt.title(title)
    plt.xlabel(column_x)
    plt.ylabel(column_y)
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.show()
