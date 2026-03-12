import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
# === 确保全局全部使用 Arial 字体 ===
plt.rcParams["font.family"] = "Arial"
# === 读取矩阵数据 ===
matrix = np.loadtxt('D:/Python/pycharm/nas/correlation/correlation_matrix.txt')  # 读取矩阵

matrix = np.rot90(matrix)

# === 上下翻转矩阵 ===
matrix = matrix[::-1]  # 将矩阵上下翻转

# === 获取矩阵的尺寸 ===
Ny, Nx = matrix.shape  # 获取矩阵的行数和列数

# === 创建坐标轴 ===
x = np.linspace(-6, -2, Nx)
y = np.linspace(-6, -2, Ny)

# 使用meshgrid生成网格
xv, yv = np.meshgrid(x, y)

# === 设置手动的v_max和v_min ===
v_min = -0.2  # 用户手动设置 v_min
v_max = 0.2  # 用户手动设置 v_max

# === 设置手动的坐标轴范围 ===
x_min = -6  # 用户手动设置x轴最小值
x_max = -2  # 用户手动设置x轴最大值
y_min = -6  # 用户手动设置y轴最小值
y_max = -2  # 用户手动设置y轴最大值

# === 坐标轴物理长度（英寸） ===
x_axis_inches = 2.5 # 横轴长度
y_axis_inches = 2.5  # 纵轴长度
left_margin = 0.65
right_margin = 0.3
top_margin = 0.3
bottom_margin = 0.65

fig_width = left_margin + x_axis_inches + right_margin
fig_height = bottom_margin + y_axis_inches + top_margin

fig = plt.figure(figsize=(fig_width, fig_height), dpi=200)

# === 设置绘图区域大小 ===
x0 = left_margin / fig_width
y0 = bottom_margin / fig_height
w = x_axis_inches / fig_width
h = y_axis_inches / fig_height
ax = fig.add_axes([x0, y0, w, h])  # 仅控制坐标轴区域大小

# === 设置坐标轴字体和大小 ===
x_axis_font = 'Arial'
y_axis_font = 'Arial'
font_size = 12  # 设置字体大小

# # === 定义自定义色图 ===
custom_cmap = LinearSegmentedColormap.from_list("custom_red",
                                                ["#fff7e9", "#a0e4ec", "#a0e4ec",
                                                 "white", "#f7d1d1", "#ffd9d9", "#fffbf3"]
                                                )  # 自定义色带-红色黄色


# === 可视化二维网格和矩阵数据 ===

plt.pcolormesh(xv, yv, matrix, shading='auto', vmin=v_min, vmax=v_max, cmap=custom_cmap)  # 使用自定义色带

plt.xticks(
    fontsize=font_size,
)
plt.yticks(
    fontsize=font_size,
)
# === 调整坐标轴范围 ===
plt.xlim(x_min, x_max)  # 设置x轴范围
plt.ylim(y_min, y_max)  # 设置y轴范围

# === 修改坐标轴刻度字体和大小 ===
plt.xticks(fontsize=font_size, fontname=x_axis_font)  # 设置x轴刻度字体和大小
plt.yticks(fontsize=font_size, fontname=y_axis_font)  # 设置y轴刻度字体和大小
plt.xticks(np.linspace(-6, -2, 5))
plt.yticks(np.linspace(-6, -2, 5))
# === 可选：修改坐标轴刻度线的样式 ===
plt.tick_params(axis='x', labelsize=font_size, labelcolor='black')  # 设置x轴刻度线的样式
plt.tick_params(axis='y', labelsize=font_size, labelcolor='black')  # 设置y轴刻度线的样式

# === 添加颜色条（手动位置和尺寸） ===
# 颜色条位置和尺寸（以figure宽高比例表示）
# 注意：这里的位置是相对于整个figure的坐标系
cb_width_inches = 0.12   # 设置颜色条宽度（英寸）
cb_height_inches = 0.6   # 设置颜色条高度（英寸）

# 转换为 figure 坐标
cb_width = cb_width_inches / fig_width
cb_height = cb_height_inches / fig_height
cb_x = x0 + 0.02  # 相对于左下角略微右移，防止压住主图
cb_y = y0 + 0.13  # 相对于主图底部向上移动

# 添加颜色条轴
cax = fig.add_axes([cb_x, cb_y, cb_width, cb_height])  # 手动设置颜色条轴

# 添加颜色条内容
cbar = plt.colorbar(ax.collections[0], cax=cax)
cbar.ax.tick_params(labelsize=8)
cbar.set_ticks([-0.2, 0.2])

circles = [
    {
        "x": -2.82,
        "y": -4.12,
        "radius": 0.06,
        "edgecolor": "#1150A3",
        "linewidth": 0.8,
        "linestyle": "-",
        "draw_dashed": False,
        "dashed_color": "#C8227D",
        "dashed_style": "--",
        "dashed_width": 0.8,
    },
    {
        "x": -2.82,
        "y": -5.55,
        "radius": 0.06,
        "edgecolor": "#1150A3",
        "linewidth": 0.8,
        "linestyle": "-",
        "draw_dashed": False,
        "dashed_color": "#C8227D",
        "dashed_style": "--",
        "dashed_width": 0.8,
    },
]

# ========================================================
# 绘制多个圆圈及其投影虚线
# ========================================================
for c in circles:
    # --- 画圆圈 ---
    circle = plt.Circle(
        (c["x"], c["y"]),
        radius=c["radius"],
        edgecolor=c.get("edgecolor", "#0EE8E8"),
        facecolor="none",
        linewidth=c.get("linewidth", 1.2),
        linestyle=c.get("linestyle", "-"),
        zorder=10
    )
    ax.add_patch(circle)

    # --- 虚线投影（可关闭） ---
    if c.get("draw_dashed", False):
        # 垂直线
        ax.plot(
            [c["x"], c["x"]],
            [y_min, c["y"]],
            linestyle=c.get("dashed_style", "--"),
            linewidth=c.get("dashed_width", 0.8),
            color=c.get("dashed_color", c.get("edgecolor", "#0EE8E8")),
            zorder=5
        )

        # 水平线
        ax.plot(
            [x_min, c["x"]],
            [c["y"], c["y"]],
            linestyle=c.get("dashed_style", "--"),
            linewidth=c.get("dashed_width", 0.8),
            color=c.get("dashed_color", c.get("edgecolor", "#0EE8E8")),
            zorder=5
        )

ax.set_xlabel('Conductance / log(G/G$_0$)', fontname=x_axis_font, fontsize=font_size)   # 设置x轴标签字体和大小
ax.set_ylabel('Conductance / log(G/G$_0$)', fontname=y_axis_font, fontsize=font_size)   # 设置y轴标签字体和大小


plt.show()
# plt.savefig("corr.png", dpi=300, transparent=True)