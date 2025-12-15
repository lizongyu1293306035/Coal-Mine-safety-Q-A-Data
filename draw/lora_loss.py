import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 设置中文字体（如果需要显示中文）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
# 设置全局字体大小
plt.rcParams.update({
    'font.family': 'Times New Roman',  # 设置字体为 Times New Roman
    # 'font.size': 14,           # 全局字体大小
    # 'axes.titlesize': 16,      # 标题字体大小
    # 'axes.labelsize': 15,      # 坐标轴标签字体大小
    'xtick.labelsize': 20,  # x轴刻度标签字体大小
    'ytick.labelsize': 20,  # y轴刻度标签字体大小
    'legend.fontsize': 20  # 图例字体大小
})


# 从Excel文件读取数据
def read_loss_data(file_path):
    """
    从Excel文件读取loss数据
    文件格式应该包含 'step' 和 'loss' 两列
    """
    try:
        # 读取Excel文件
        df = pd.read_excel(file_path)
        print("文件读取成功！")
        print(f"数据形状: {df.shape}")
        print("\n前5行数据:")
        print(df.head())

        # 检查必要的列是否存在
        if 'step' not in df.columns or 'loss' not in df.columns:
            raise ValueError("Excel文件中必须包含 'step' 和 'loss' 两列")

        return df['step'].values, df['loss'].values

    except FileNotFoundError:
        print(f"错误：找不到文件 {file_path}")
        return None, None
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return None, None


# 绘制专业的loss曲线图
def plot_loss_curve(steps, losses, save_path=None):
    """
    绘制专业美观的loss曲线图
    """
    if steps is None or losses is None:
        print("无法绘制图表：数据为空")
        return

    # 创建图表，设置尺寸和分辨率
    plt.figure(figsize=(10, 6), dpi=100)

    # 绘制loss曲线
    plt.plot(steps, losses,
             linewidth=2.5,
             color='#2E86AB',  # 专业的蓝色
             # marker='o',  # 数据点标记
             markersize=4,
             markerfacecolor='#F24236',  # 标记颜色
             markeredgewidth=0.5,
             markeredgecolor='white',
             alpha=0.8,
             label='Training Loss')

    # 设置标题和标签
    plt.xlabel('Training Steps', fontsize=14, fontweight='bold')
    plt.ylabel('Loss Value', fontsize=14, fontweight='bold')
    plt.title('Training Loss Curve', fontsize=16, fontweight='bold', pad=20)

    # 设置网格
    plt.grid(True,
             linestyle='--',
             alpha=0.7,
             color='gray',
             linewidth=0.5)

    # 设置坐标轴范围
    plt.xlim(left=min(steps) - 1, right=max(steps) + 1)
    plt.ylim(bottom=0, top=max(losses) * 1.1)  # 留10%的顶部空间

    # 美化坐标轴
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(0.5)
    ax.spines['bottom'].set_linewidth(0.5)

    # 设置刻度
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    # 添加图例
    plt.legend(fontsize=12, frameon=True, fancybox=True, shadow=True)

    # 自动调整布局
    plt.tight_layout()

    # 保存图片
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"图表已保存至: {save_path}")

    # 显示图表
    plt.show()

    return ax


# 绘制平滑的loss曲线（可选）
def plot_smoothed_loss_curve(steps, losses, window_size=5, save_path=None):
    """
    绘制平滑后的loss曲线
    """
    if steps is None or losses is None:
        print("无法绘制图表：数据为空")
        return

    # 计算滑动平均
    if len(losses) > window_size:
        smoothed_losses = np.convolve(losses, np.ones(window_size) / window_size, mode='valid')
        smoothed_steps = steps[window_size - 1:]
    else:
        smoothed_losses = losses
        smoothed_steps = steps

    # 创建图表
    plt.figure(figsize=(10, 6), dpi=100)

    # 绘制原始数据（半透明）
    plt.plot(steps, losses,
             alpha=0.5,
             color='blue',
             linewidth=1,
             label='Original Loss')

    # 绘制平滑曲线
    plt.plot(smoothed_steps, smoothed_losses,
             linewidth=2.5,
             color='#E63946',  # 红色
             label=f'Smoothed Loss')

    # 设置标题和标签
    plt.xlabel('Steps', fontsize=25, fontweight='bold')
    plt.ylabel('Loss Value', fontsize=25, fontweight='bold')
    plt.title('Training Loss Curve', fontsize=25, fontweight='bold', pad=20)

    # 设置网格和其他美化
    # plt.grid(True, linestyle='--', alpha=0.7)
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # 添加图例
    plt.legend(fontsize=24)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"平滑图表已保存至: {save_path}")

    plt.show()


# 主程序
def main():
    # 文件路径
    file_path = 'result_file/lora_loss.xlsx'

    # 读取数据
    steps, losses = read_loss_data(file_path)

    if steps is not None and losses is not None:
        print(f"\n成功读取 {len(steps)} 个数据点")
        print(f"Step范围: {min(steps)} - {max(steps)}")
        print(f"Loss范围: {min(losses):.4f} - {max(losses):.4f}")

        # 绘制原始loss曲线
        # plot_loss_curve(steps, losses, 'loss_curve.png')

        # 绘制平滑loss曲线（如果数据点足够多）
        if len(steps) > 10:
            plot_smoothed_loss_curve(steps, losses, window_size=10, save_path='smoothed_loss_curve.png')

        # 打印统计信息
        print("\n=== 统计信息 ===")
        print(f"最终Loss: {losses[-1]:.6f}")
        print(f"最小Loss: {min(losses):.6f}")
        print(f"平均Loss: {np.mean(losses):.6f}")
        print(f"Loss下降比例: {(losses[0] - losses[-1]) / losses[0] * 100:.2f}%")


# 如果直接运行此脚本，执行主程序
if __name__ == "__main__":
    main()
