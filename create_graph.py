import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from aiogram.types import FSInputFile

# def cmd_graph(categories, moneys, user_id):
#     try:
#         labels = []
#         for i in categories:
#             labels.append(i[0])
#         fig, ax = plt.subplots(figsize=(7, 4))
#         fig.patch.set_facecolor('#8a8389')
#         ax.set_position([0.1, 0, 1, 1])  # [left, bottom, width, height]
#         ax.pie(moneys,
#                labels=None,
#                autopct=lambda p: f'{int(p/100.*sum(moneys))}' if p > 0 else None,
#                shadow=True)
#         ax.legend(labels, title="Категории", loc="center left", bbox_to_anchor=(0, 0.5))
#         ax.axis('equal')
#         plt.title("Ваши расходы")
#         plt.savefig(f'graph/graph_test_{user_id}.png')
#         plt.close()
#         photo = FSInputFile(f"graph/graph_test_{user_id}.png")
#         return photo
#     except Exception:
#         return None


def cmd_graph(categories, moneys, user_id):
    try:
        labels = [category[0] if isinstance(category, (tuple, list)) else category
                  for category in categories]

        fig_width = max(6, len(labels) * 0.8)
        fig, ax = plt.subplots(figsize=(fig_width, 5))
        fig.patch.set_facecolor('#F5F5F5')

        colors = plt.cm.tab20.colors[:len(labels)]

        bars = ax.bar(labels, moneys, color=colors)

        ax.set_title("Ваши расходы по категориям", pad=20)
        ax.set_ylabel("Сумма (руб)", labelpad=10)

        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=70, ha='right', rotation_mode='anchor')

        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + max(moneys) * 0.001,
                f'{int(height)}',
                ha='center',
                va='bottom',
                fontsize=10
            )

        plt.tight_layout()

        file_path = f'graph/graph_test_{user_id}.png'
        plt.savefig(file_path, bbox_inches='tight', dpi=100)
        plt.close()

        return FSInputFile(file_path)
    except Exception as e:
        print(f"Ошибка при построении графика: {e}")
        return None