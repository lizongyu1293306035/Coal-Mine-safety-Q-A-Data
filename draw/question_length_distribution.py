# coding:utf-8
"""
@Filename: question_length_distribution.py
@Description: 绘制问题长度分布曲线图
@Author: Li Zongyu
@Time: 2025/10/16 20:57
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# 使用seaborn风格的版本
def read_data_and_plot_two_files_seaborn(filename1, filename2, label1='文件1', label2='文件2'):
    try:
        # 设置seaborn风格
        sns.set_style("whitegrid")

        # 读取两个Excel文件
        df1 = pd.read_excel(filename1)
        df2 = pd.read_excel(filename2)

        # 检查文件是否包含需要的列
        for df, filename in [(df1, filename1), (df2, filename2)]:
            if 'length' not in df.columns or 'count' not in df.columns:
                print(f"文件 {filename} 中未找到 'length' 和 'count' 列")
                print(f"文件中的列名：", df.columns.tolist())
                return

        # 提取数据
        length1 = df1['length']
        count1 = df1['count']
        length2 = df2['length']
        count2 = df2['count']

        print("成功读取数据：")
        print(f"{label1}: {len(df1)} 条记录")
        print(f"{label2}: {len(df2)} 条记录")

        # 绘制曲线图
        plt.figure(figsize=(14, 7))

        # 绘制两条曲线，使用不同的样式
        plt.plot(length1, count1, linewidth=2.5, markersize=8,
                 markerfacecolor='#FF6B6B', markeredgecolor='#FF6B6B', color='#4ECDC4',
                 label=label1, alpha=0.8)

        plt.plot(length2, count2, linewidth=2.5, markersize=8,
                 markerfacecolor='#45B7D1', markeredgecolor='#45B7D1', color='#96CEB4',
                 label=label2, alpha=0.8)

        plt.title('Length vs Count 曲线对比图', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Length', fontsize=13)
        plt.ylabel('Count', fontsize=13)
        plt.grid(True, alpha=0.4)

        # 设置横坐标以10为单位
        all_lengths = pd.concat([length1, length2])
        max_length = max(all_lengths)
        # 计算合适的刻度间隔，确保以10为单位
        tick_interval = 100
        plt.xticks(np.arange(0, max_length + tick_interval, tick_interval))

        # 添加图例
        plt.legend(fontsize=12, loc='best')

        # 设置y轴从0开始
        plt.ylim(bottom=0)

        # 添加一些统计信息到图例或标题
        total1 = count1.sum()
        total2 = count2.sum()
        plt.figtext(0.02, 0.02, f'{label1}总数: {total1} | {label2}总数: {total2}',
                    fontsize=10, alpha=0.7)

        plt.tight_layout()
        plt.show()

    except FileNotFoundError as e:
        print(f"文件未找到: {e}")
    except Exception as e:
        print(f"出错: {e}")


# 使用示例
read_data_and_plot_two_files_seaborn(
    r"../data/data_distribution/question_distribution.xlsx",
    r"../data/data_distribution/answer_distribution.xlsx",  # 替换为第二个文件路径
    "Question",
    "Answer"
)