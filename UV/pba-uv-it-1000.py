import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import numpy as np
from scipy.signal import savgol_filter

# === 确保全局全部使用 Arial 字体 ===
plt.rcParams["font.family"] = "Arial"

# === 1. 设定数据文件所在文件夹路径 ===
data_folder = "D:/Python/pycharm/nas/UV"

# === 2. 搜索所有 txt 文件 ===
files = glob.glob(os.path.join(data_folder, "*.txt"))

# === 手动指定绘制顺序（文件名不含扩展名） ===
custom_order = ["0.0 V", "-0.2 V", "-0.6 V",
                "-1.0 V", "-1.2 V", "-1.4 V", "-1.6 V"]

# === 手动指定颜色 ===
custom_colors = {
    "0.0 V": "#D28888",
    "-0.2 V": "#D2888888",
    "-0.6 V": "#D2888855",
    "-1.0 V": "#33848D44",
    "-1.2 V": "#33848D66",
    "-1.4 V": "#33848D88",
    "-1.6 V": "#33848D",
}

# === 生成文件名映射表 ===
file_labels = {os.path.splitext(os.path.basename(f))[0]: f for f in files}

# === 按自定义顺序排序 ===
ordered_files = []
for name in custom_order:
    if name in file_labels:
        ordered_files.append(file_labels[name])
for name, f in file_labels.items():
    if name not in custom_order:
        ordered_files.append(f)

# === 图像与字体参数 ===
font_size = 12

# === 坐标轴范围设置 ===
x_min, x_max = 190, 650
y_min, y_max = -0.0, 1.2

# === 坐标轴物理长度（英寸） ===
x_axis_inches = 2.5
y_axis_inches = 2
left_margin = 0.5
right_margin = 0.3
top_margin = 0.3
bottom_margin = 0.5

fig_width = left_margin + x_axis_inches + right_margin
fig_height = bottom_margin + y_axis_inches + top_margin

# === 创建图形 ===
fig = plt.figure(figsize=(fig_width, fig_height), dpi=200)
ax = fig.add_axes([
    left_margin / fig_width,
    bottom_margin / fig_height,
    x_axis_inches / fig_width,
    y_axis_inches / fig_height
])

# === 存储绘图句柄和标签 ===
handles = []
labels_in_order = []

# === 3. 按顺序读取数据并绘制 ===
for file in ordered_files:
    label = os.path.splitext(os.path.basename(file))[0]

    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if "Wavelength" in line:
            start_index = i + 1
            break

    data = pd.read_csv(file, skiprows=start_index, names=["Wavelength", "Abs"], encoding='utf-8')

    try:
        smooth_abs = savgol_filter(data["Abs"], window_length=31, polyorder=3)
    except ValueError:
        smooth_abs = data["Abs"].values

    min_val = np.min(smooth_abs)
    max_val = np.max(smooth_abs)
    if max_val > min_val:
        norm_abs = (smooth_abs - min_val) / (max_val - min_val)
    else:
        norm_abs = smooth_abs * 0

    color = custom_colors.get(label, None)

    line = ax.plot(
        data["Wavelength"],
        norm_abs,
        linewidth=1.2,
        color=color
    )

    # 存储句柄和标签
    handles.append(line[0])
    labels_in_order.append(label)

# === 修改坐标刻度字体 ===
plt.xticks(
    ticks=np.linspace(200, 600, 5),
    fontsize=font_size - 0,
)
plt.yticks(
    fontsize=font_size - 2,
)

# === 4. 坐标轴与样式美化 ===
ax.set_xlabel("Wavelength / nm", fontsize=font_size)
ax.set_ylabel("Normalized Absorbance", fontsize=font_size)
ax.yaxis.set_label_coords(-0.05, 0.5)

ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_yticks([])

# === 5. 创建自定义图例实现右对齐效果 ===
# 方法1：使用右对齐文本
fig.canvas.draw()  # 确保图形已渲染

# 创建图例，使用等宽字体或手动调整间距
# 获取当前图形的渲染器
renderer = fig.canvas.get_renderer()

# 方法2：使用LaTeX空格实现右对齐（更简单可靠）
# 在"0.0 V"前添加空格使其与负号对齐
aligned_labels = []
for label in labels_in_order:
    if label == "0.0 V":
        # 添加空格使"0"对齐到负号位置
        aligned_labels.append(r"$\;$0.0 V")  # 使用LaTeX空格
    else:
        aligned_labels.append(label)

# 手动控制图例位置
legend_x = 0.84  # 横向位置（0~1，基于坐标轴 Axes 范围）
legend_y = 0.64  # 纵向位置（0~1）

# 创建图例
legend = ax.legend(
    handles,
    aligned_labels,
    fontsize=font_size - 2.5,
    loc="center",
    bbox_to_anchor=(legend_x, legend_y),
    frameon=False,
    handlelength=2.0,  # 控制线条长度
    handletextpad=0.5,  # 控制线条和文本之间的间距
)

# 或者使用更简单的方法：直接修改图例文本的ha（水平对齐）属性
# 但这种方法的对齐效果不如上面添加空格的方法精确

ax.tick_params(labelsize=font_size - 0)

# === 5. 显示图像 ===
# plt.show()
plt.savefig("UV.png", dpi=300, transparent=True)
