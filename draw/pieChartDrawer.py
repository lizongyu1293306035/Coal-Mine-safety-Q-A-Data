# coding:utf-8
"""
@Filename: pieChartDrawer.py
@Description: 绘制饼状图
@Author: Li Zongyu
@Time: 2025/10/19 11:46
"""

import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体和科研风格
plt.rcParams['font.sans-serif'] = ['SimSun', 'Times New Roman']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 数据
categories = ['煤矿安全法规制度类问题', '煤矿安全操作规程类问题', '煤矿安全名词术语解释类问题']
values = [11797, 10564, 3155]

# 科研配色方案（使用更加专业的颜色）
colors = ['#efd1cc', '#ad9981', '#927995']  # 深蓝、紫红、橙色

# 创建图形
fig, ax = plt.subplots(figsize=(10, 8), dpi=100)

# 绘制饼图
wedges, texts, autotexts = ax.pie(values,
                                  # labels=categories,
                                  colors=colors,
                                  autopct='%1.1f%%',
                                  startangle=90,
                                  textprops={'fontsize': 60, "fontfamily": "Times New Roman"})

# 设置标题
# plt.title('煤矿安全问题类型分布', fontsize=16, fontweight='bold', pad=20)

# 美化文字
for autotext in autotexts:
    autotext.set_color('black')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(14)

for text in texts:
    text.set_fontsize(14)

# 添加图例
legend = ax.legend(wedges, [f'{cat}\n({val}个, {val / sum(values) * 100:.1f}%)'
                            for cat, val in zip(categories, values)],
                   # title="问题类型",
                   loc="center left",
                   bbox_to_anchor=(1, 0, 0.5, 1),
                   fontsize=14)
for text in legend.get_texts():
    text.set_fontsize(10.5)
    text.set_fontfamily(["SimSun", "Arial"])  # 英文字体
    # text.set_color('#2F2F2F')  # 文字颜色
    # text.set_alpha(0.9)           # 文字透明度
# 确保饼图是圆形
ax.set_aspect('equal')

# 调整布局
plt.tight_layout()

# 显示图形
plt.show()

# 可选：保存图片
# plt.savefig('煤矿安全问题分布饼图.png', bbox_inches='tight', dpi=300)
