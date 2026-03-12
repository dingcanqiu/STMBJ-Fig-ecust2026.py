import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.optimize import curve_fit
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# === 确保全局全部使用 Arial 字体 ===
plt.rcParams["font.family"] = "Arial"
# === 定义2D高斯函数 ===
def gaussian_2d(coords, amplitude, xo, yo, sigma_x, sigma_y, theta, offset):
    x, y = coords
    xo = float(xo)
    yo = float(yo)
    a = (np.cos(theta) ** 2) / (2 * sigma_x ** 2) + (np.sin(theta) ** 2) / (2 * sigma_y ** 2)
    b = -(np.sin(2 * theta)) / (4 * sigma_x ** 2) + (np.sin(2 * theta)) / (4 * sigma_y ** 2)
    c = (np.sin(theta) ** 2) / (2 * sigma_x ** 2) + (np.cos(theta) ** 2) / (2 * sigma_y ** 2)
    g = offset + amplitude * np.exp(
        - (a * (x - xo) ** 2 + 2 * b * (x - xo) * (y - yo) + c * (y - yo) ** 2))
    return g.ravel()


# === 读取矩阵数据 ===
matrix = np.loadtxt('D:/Python/pycharm/nas/PSD/psdStaticAnalysis.txt')  # 读取矩阵
matrix = np.rot90(matrix)
matrix = matrix[::-1]

Ny, Nx = matrix.shape
x = np.linspace(-4, -1.5, Nx)
y = np.linspace(-4.5, 1.5, Ny)
xv, yv = np.meshgrid(x, y)

# === 高斯拟合 ===
initial_guess = (np.max(matrix), -3, -3, 1, 1, 0, 0)
popt, pcov = curve_fit(gaussian_2d, (xv.ravel(), yv.ravel()), matrix.ravel(), p0=initial_guess)

# === 在更细网格上重采样（保证等势线更顺滑） ===
x_fine = np.linspace(-4, -1.5, 200)  # 横向细化为200点
y_fine = np.linspace(-4.5, 1.5, 200)   # 纵向细化为200点
xv_fine, yv_fine = np.meshgrid(x_fine, y_fine)
fit_data_fine = gaussian_2d((xv_fine, yv_fine), *popt).reshape(200, 200)

# === 手动范围设置 ===
v_min = 0
v_max = 10
x_min, x_max = -4, -1.5
y_min, y_max = -4.5, 1.5

# === 坐标轴物理长度（保持不变） ===
x_axis_inches = 2.5
y_axis_inches = 2
left_margin = 0.7
right_margin = 0.3
top_margin = 0.3
bottom_margin = 0.5

fig_width = left_margin + x_axis_inches + right_margin
fig_height = bottom_margin + y_axis_inches + top_margin

fig = plt.figure(figsize=(fig_width, fig_height), dpi=200)

x0 = left_margin / fig_width
y0 = bottom_margin / fig_height
w = x_axis_inches / fig_width
h = y_axis_inches / fig_height
ax = fig.add_axes([x0, y0, w, h])

# === 字体和色图 ===
x_axis_font = 'Arial'
y_axis_font = 'Arial'
font_size = 12
custom_cmap = LinearSegmentedColormap.from_list("custom_red", ["white", "#70d1dc", "#fff7e9"])

# === 原始矩阵图 ===
c = ax.pcolormesh(xv, yv, matrix, shading='auto', vmin=v_min, vmax=v_max, cmap=custom_cmap)

# === 在坐标轴内左下角添加 inset colorbar ===
cax = inset_axes(
    ax,
    width="5%",      # 颜色条宽度（相对 ax 宽度百分比）
    height="20%",      # 颜色条高度（相对 ax 高度百分比）
    loc="lower left", # 左下角
    bbox_to_anchor=(0.05, 0.05, 1, 1),  # (x偏移, y偏移, 宽, 高)
    bbox_transform=ax.transAxes,
    borderpad=0
)

cb = plt.colorbar(
    c,
    cax=cax,
    orientation="vertical"  # 横向颜色条（左下角通常更美观）
)

cb.set_ticks([v_min, v_max])
cb.ax.tick_params(labelsize=10)


# === 添加顺滑的高斯拟合黑色等势线 ===
contours = ax.contour(xv_fine, yv_fine, fit_data_fine,
                      levels=[0.5, 2, 4, 7, 9.6],
                      colors='black', linewidths=0.6)

# === 坐标轴设置 ===
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_xlabel('Conductance / log(G/G$_0$)', fontname=x_axis_font, fontsize=font_size)
ax.set_ylabel('Noise power / log(G/G$_0$)', fontname=y_axis_font, fontsize=font_size)

ax.set_xticks(np.linspace(-4, -2, 3))
ax.set_yticks(np.linspace(-4, 1, 6))
ax.tick_params(axis='x', labelsize=12, labelcolor='black')
ax.tick_params(axis='y', labelsize=12, labelcolor='black')


ax.text(
    0.9, 0.9,              # 右上角（Axes 坐标）
    r'n = 1.18',             # 显示内容（r'' 便于以后写数学公式）
    transform=ax.transAxes,  # 使用 Axes 归一化坐标
    ha='right',              # 水平右对齐
    va='top',                # 垂直顶对齐
    fontsize=12,
    fontname='Arial',
    color='black'
)

plt.show()
# plt.savefig("psd.png", dpi=300, transparent=True)