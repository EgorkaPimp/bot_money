import matplotlib.pyplot as plt
from aiogram.types import FSInputFile

def cmd_graph(categories, moneys, user_id):
    try:
        labels = []
        for i in categories:
            labels.append(i[0])
        fig, ax = plt.subplots(figsize=(7, 4))
        fig.patch.set_facecolor('#8a8389')
        ax.set_position([0.1, 0, 1, 1])  # [left, bottom, width, height]
        ax.pie(moneys,
               labels=None,
               autopct=lambda p: f'{int(p/100.*sum(moneys))}' if p > 0 else None,
               shadow=True)
        ax.legend(labels, title="Категории", loc="center left", bbox_to_anchor=(0, 0.5))
        ax.axis('equal')
        plt.title("Ваши расходы")
        plt.savefig(f'graph/graph_test_{user_id}.png')
        plt.close()
        photo = FSInputFile(f"graph/graph_test_{user_id}.png")
        return photo
    except Exception:
        return None