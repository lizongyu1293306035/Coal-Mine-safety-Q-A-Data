# coding:utf-8
"""
@Filename: gspo_result.py
@Description:
@Author: Li Zongyu
@Time: 2025/9/25 21:05
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 设置全局字体大小
plt.rcParams.update({
    'font.family': 'Times New Roman',  # 设置字体为 Times New Roman
    # 'font.size': 14,           # 全局字体大小
    # 'axes.titlesize': 16,      # 标题字体大小
    # 'axes.labelsize': 15,      # 坐标轴标签字体大小
    'xtick.labelsize': 20,  # x轴刻度标签字体大小
    'ytick.labelsize': 20,  # y轴刻度标签字体大小
    # 'legend.fontsize': 12      # 图例字体大小
})
# 读取文件
data = pd.read_excel(r'result_file/gspo_result.xlsx')

# 创建包含两个子图的图形
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# 设置每隔多少步标记一个marker
marker_interval = 100

# 绘制Training Loss曲线
marker_positions = np.where(data['Step'] % marker_interval == 0)[0]
ax1.plot(data['Step'], data['Training Loss'], color='blue',
         marker='o', markevery=marker_positions, markersize=6)
ax1.set_xlabel('Step', fontsize=25)
ax1.set_ylabel('Training Loss', fontsize=25)
ax1.set_title('Training Curve', fontsize=25)
# ax1.grid(True, linestyle='--', alpha=0.7)

# 绘制Reward曲线
ax2.plot(data['Step'], data['reward'], color='red',
         marker='s', markevery=marker_positions, markersize=6)
ax2.set_xlabel('Step', fontsize=25)
ax2.set_ylabel('Reward', fontsize=25)
ax2.set_title('Reward Curve', fontsize=25)
# ax2.grid(True, linestyle='--', alpha=0.7)

# 调整布局
plt.tight_layout()
plt.show()
