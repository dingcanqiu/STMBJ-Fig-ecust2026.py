import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# === 确保全局全部使用 Arial 字体 ===
plt.rcParams["font.family"] = "Arial"

# ================ 公共设置 ================
x_axis_inches = 2.5
y_axis_inches = 2.3
left_margin = 0.7
right_margin = 0.3
top_margin = 0.3
bottom_margin = 0.5
vertical_gap_inches = 0.0   # 两图之间的间距（英寸）

# 计算总高度：上下两图 + 间距 + 上下边距
fig_width = left_margin + x_axis_inches + right_margin
fig_height = bottom_margin + y_axis_inches*2 + vertical_gap_inches + top_margin

fig = plt.figure(figsize=(fig_width, fig_height), dpi=100)

# ========= 子图区域位置（手动 add_axes） =========
x0 = left_margin / fig_width
w = x_axis_inches / fig_width
h = y_axis_inches / fig_height
gap = vertical_gap_inches / fig_height

# 上图位置
y0_top = bottom_margin/fig_height + h
ax1 = fig.add_axes([x0, y0_top, w, h])

# 下图位置（共用 x 轴）
y0_bottom = bottom_margin / fig_height
ax2 = fig.add_axes([x0, y0_bottom, w, h], sharex=ax1)

# =============== 读取与绘制函数封装（完全保留你原来的风格） ===============
def plot_matrix(ax, filepath, custom_cmap, v_max):
    matrix = np.loadtxt(filepath)
    matrix = np.rot90(matrix)
    matrix = matrix[::-1]

    Ny, Nx = matrix.shape
    x = np.linspace(-4.93e-01, 3.0, Nx)
    y = np.linspace(-9.989, 1, Ny)
    xv, yv = np.meshgrid(x, y)

    v_min = 0

    x_min, x_max = -0.1, 0.65
    y_min, y_max = -6.5, 0.5

    font_size = 12
    x_axis_font = 'Arial'
    y_axis_font = 'Arial'

    pcm = ax.pcolormesh(xv, yv, matrix, shading='auto',
                        vmin=v_min, vmax=v_max, cmap=custom_cmap)

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xticks(np.linspace(0, 0.6, 5))
    ax.set_yticks(np.linspace(-6, 0, 4))

    ax.tick_params(axis='x', labelsize=font_size, labelcolor='black')
    ax.tick_params(axis='y', labelsize=font_size, labelcolor='black')

    # ax.set_ylabel('Conductance / log(G/G$_0$)',
    #               fontname=y_axis_font, fontsize=font_size)

    return pcm

# ==================== 上图 ====================
cmap_top = LinearSegmentedColormap.from_list("c1",
            ["white", "#BBDFC9", "#F9F8D8"])

pcm1 = plot_matrix(ax1,
                   'D:/Python/pycharm/nas/1D,2D-histograms-组合图/3-pa/WA-BJ_3Dhist.txt',
                   cmap_top, v_max=200)

# 上图颜色条
cb_w = 0.12 / fig_width
cb_h = 0.40 / fig_height
cb_x = x0 + 0.02
cb_y = y0_top + 0.012
cax1 = fig.add_axes([cb_x, cb_y, cb_w, cb_h])
cbar1 = plt.colorbar(pcm1, cax=cax1)
cbar1.ax.tick_params(labelsize=7)
cbar1.set_ticks([0, 200])

# ==================== 下图 ====================
cmap_bottom = LinearSegmentedColormap.from_list("c2",
            ["white", "#9ec8b0", "#F9F8CA"])

pcm2 = plot_matrix(ax2,
                   'D:/Python/pycharm/nas/1D,2D-histograms-组合图/3-pba/WA-BJ_3Dhist.txt',
                   cmap_bottom, v_max=220)

# 下图颜色条
cb_y2 = y0_bottom + 0.012
cax2 = fig.add_axes([cb_x, cb_y2, cb_w, cb_h])
cbar2 = plt.colorbar(pcm2, cax=cax2)
cbar2.ax.tick_params(labelsize=7)
cbar2.set_ticks([0, 220])

# ========== 仅底部图添加 X 轴标签 ==========
ax2.set_xlabel('ΔZ / nm', fontname='Arial', fontsize=12)

# ========== 让上图不显示 X 轴刻度标签（一致美观） ==========
plt.setp(ax1.get_xticklabels(), visible=False)

# === 计算两个子图覆盖区域的中心 Y 值 ===
y_center = y0_bottom + h   # 两个子图的整体中点

# === 添加全局纵坐标标签（在子图区域的中间位置） ===
fig.text(
    0.08,           # x 坐标，你可微调，比如 0.07 或 0.09
    y_center,       # 使用子图区域的中心
    'Conductance / log(G/G$_0$)',
    va='center', ha='center',
    rotation='vertical',
    fontsize=12, fontname='Arial'
)

plt.show()
# plt.savefig("2d-squ.png", dpi=300, transparent=True)