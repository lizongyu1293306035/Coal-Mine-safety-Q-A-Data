# coding:utf-8
"""
@Filename: boxPlotDrawer.py
@Description: 画箱型图的脚本
@Author: Li Zongyu
@Time: 2025/10/17 9:03
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 设置中文字体和样式
plt.rcParams['font.sans-serif'] = ['SimSun']
plt.rcParams['axes.unicode_minus'] = False

def algorithm(n, m, interference_pairs, iterate_count, tabu_tenure=50):

    pass


def read_data_from_excel(file_path):

    """从Excel文件读取数据并展开为列表"""
    df = pd.read_excel(file_path)
    data = []
    for _, row in df.iterrows():
        data.extend([row['length']] * int(row['count']))
    return data


# 从两个Excel文件读取数据
data1 = read_data_from_excel(r'../data/data_distribution/question_distribution.xlsx')
data2 = read_data_from_excel(r'../data/data_distribution/answer_distribution.xlsx')

# 准备绘图数据
all_data = [data1, data2]
labels = ['Question', 'Answer']

# 创建图形
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# 第一个子图：箱形图对比（不显示异常值）
colors = ['#3174a1', '#e1812d']
box_plot = ax1.boxplot(all_data,
                       vert=True,
                       patch_artist=True,
                       labels=labels,
                       widths=0.6,
                       showmeans=True,
                       showfliers=False,  # 不显示异常值点
                       meanprops={'marker': 'D', 'markerfacecolor': 'gold', 'markersize': 8})

for label in ax1.get_xticklabels():
    label.set_fontsize(24)
    label.set_fontfamily('Times New Roman')
    label.set_fontweight('bold')

for label in ax1.get_yticklabels():
    label.set_fontsize(24)
    label.set_fontfamily('Times New Roman')
    label.set_fontweight('bold')

# 美化箱形图
for patch, color in zip(box_plot['boxes'], colors):
    patch.set_facecolor(color)
    # patch.set_alpha(0.7)
    patch.set_edgecolor('black')
    patch.set_linewidth(2)

for whisker in box_plot['whiskers']:
    whisker.set_color('black')
    whisker.set_linewidth(2)

for cap in box_plot['caps']:
    cap.set_color('black')
    cap.set_linewidth(2)

for median in box_plot['medians']:
    median.set_color('black')
    median.set_linewidth(2)

# ax1.set_title('句子长度分布箱形图对比', fontsize=16, fontweight='bold', pad=20)
ax1.set_ylabel('Sentence Length', fontsize=24, fontfamily="Times New Roman", fontweight='bold')
# ax1.set_xlabel('问题类型', fontsize=24, fontweight='bold')
ax1.grid(axis='y', linestyle='--', alpha=0.3, color='gray')
ax1.set_axisbelow(True)

# 添加数据点散点图（抖动图）- 可选，如果也不要散点图可以注释掉
# for i, data in enumerate(all_data, 1):
#     x = np.random.normal(i, 0.08, size=len(data))  # 添加轻微抖动
#     ax1.scatter(x, data, alpha=0.4, color=colors[i - 1], s=30, zorder=0)

# 第二个子图：统计信息表格
stats_data = []
for i, (data, label) in enumerate(zip(all_data, labels)):
    stats = {
        '数据集': label,
        '样本数': len(data),
        '最小值': np.min(data),
        'Q1': np.percentile(data, 25),
        '中位数': np.median(data),
        'Q3': np.percentile(data, 75),
        '最大值': np.max(data),
        '平均值': np.mean(data)
    }
    stats_data.append(stats)

# 隐藏第二个子图的坐标轴
ax2.axis('tight')
ax2.axis('off')

# 创建表格
table_data = []
headers = ['统计量', 'Question', 'Answer']
stats_metrics = ['样本数量', '最小值', '第一四分位数', '中位数', '第三四分位数', '最大值', '平均值']

for metric in stats_metrics:
    row = [metric]
    for stats in stats_data:
        if metric == '样本数量':
            row.append(f"{stats['样本数']:,}")
        elif metric == '最小值':
            row.append(f"{stats['最小值']:.1f}")
        elif metric == '第一四分位数':
            row.append(f"{stats['Q1']:.1f}")
        elif metric == '中位数':
            row.append(f"{stats['中位数']:.1f}")
        elif metric == '第三四分位数':
            row.append(f"{stats['Q3']:.1f}")
        elif metric == '最大值':
            row.append(f"{stats['最大值']:.1f}")
        elif metric == '平均值':
            row.append(f"{stats['平均值']:.2f}")
    table_data.append(row)

table = ax2.table(cellText=table_data,
                  colLabels=headers,
                  cellLoc='center',
                  loc='center',
                  bbox=[0, 0, 1, 1])

table.auto_set_font_size(False)
table.set_fontsize(24)
table.scale(1, 1.8)

# 设置表格样式
# for i in range(len(headers)):
#     table[(0, i)].set_text_props(weight='bold', color='white', fontfamily='SimSun', size=24)
#     table[(0, i)].set_facecolor('#2E86AB')

# 遍历表头
for i in range(len(headers)):
    if i == 0:
        table[(0, i)].get_text().set_fontfamily("SimSun")
        # table[(0, i)].get_text().set_weight('bold')
    else:
        table[(0, i)].get_text().set_fontfamily('Times New Roman')

    table[(0, i)].get_text().set_size(24)
    table[(0, i)].get_text().set_color('black')
    table[(0, i)].set_facecolor('#F8F9FA')

# 遍历表的内容
for i in range(1, len(table_data) + 1):
    for j in range(len(headers)):
        if j == 0:
            # 第一列为宋体
            table[(i, j)].get_text().set_fontfamily("SimSun")
        else:
            # 其他列都为数字，即都为新罗马字体
            table[(i, j)].get_text().set_fontfamily("Times New Roman")
        if i % 2 == 0:
            table[(i, j)].set_facecolor('#F8F9FA')

plt.tight_layout()
plt.subplots_adjust(top=0.90)

# 添加图例
from matplotlib.patches import Patch

legend_elements = [
    Patch(facecolor=colors[0], label='Question'),
    Patch(facecolor=colors[1], label='Answer'),
    plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='gold', markersize=8, label='Avg')
]
ax1.legend(
    handles=legend_elements,
    loc='upper left',
    prop={'family': 'Times New Roman', 'size': 24, 'weight': 'normal'},
    framealpha=0.9
)
plt.savefig("test2.pdf", dpi=3100, format="pdf")

plt.show()



# 在控制台也输出统计信息
print("=" * 60)
print("句子长度统计分析报告")
print("=" * 60)
for stats in stats_data:
    print(f"\n{stats['数据集']}:")
    print(f"  样本数量: {stats['样本数']:,}")
    print(f"  最小值: {stats['最小值']:.1f}")
    print(f"  第一四分位数 (Q1): {stats['Q1']:.1f}")
    print(f"  中位数 (Q2): {stats['中位数']:.1f}")
    print(f"  第三四分位数 (Q3): {stats['Q3']:.1f}")
    print(f"  最大值: {stats['最大值']:.1f}")
    print(f"  平均值: {stats['平均值']:.2f}")
print("=" * 60)
