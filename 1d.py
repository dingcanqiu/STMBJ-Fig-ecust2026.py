import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# === 确保全局全部使用 Arial 字体 ===
plt.rcParams["font.family"] = "Arial"
# === 高斯函数 ===
def gaussian(x, a, mu, sigma):
    return a * np.exp(-((x - mu)**2) / (2 * sigma**2))

# === 读取数据 ===
data = np.loadtxt('D:/Python/pycharm/nas/1D,2D-histograms/WA-BJ_logHist.txt')
x = data[:, 0]
y = data[:, 1]

# === 图像与样式参数 ===
x_axis_font = 'Arial'
y_axis_font = 'Arial'
font_size = 12
bar_color = '#DFB6BC'
x_min, x_max = -6.5, 0.5
y_min, y_max = 0, 5000

# === 坐标轴物理长度（英寸） ===
x_axis_inches = 2.5  # 横轴长度
y_axis_inches = 2  # 纵轴长度
left_margin = 0.3
right_margin = 0.3
top_margin = 0.3
bottom_margin = 0.5

fig_width = left_margin + x_axis_inches + right_margin
fig_height = bottom_margin + y_axis_inches + top_margin

fig = plt.figure(figsize=(fig_width, fig_height), dpi=200)

# === 设置绘图区域大小 ===
x0 = left_margin / fig_width
y0 = bottom_margin / fig_height
w = x_axis_inches / fig_width
h = y_axis_inches / fig_height
ax = fig.add_axes([x0, y0, w, h])  # 仅控制坐标轴区域大小

# === 图例设置 ==
legend_location = 'upper right'
legend_fontsize = 6
legend_frame = True
legend_alpha = 0.8

# === 拟合峰设置 ===
fit_peaks = [
    {'center': -3.0, 'range': 0.4, 'show': True,  'color': '#000000',  'label': 'HC'},
    {'center': -4.0, 'range': 0.4, 'show': True,  'color': '#000000', 'label': 'MC'},
    {'center': -5.3, 'range': 0.4, 'show': True,  'color': '#000000', 'label': 'LC'},
]

# === 绘制柱状图 ===
ax.bar(x, y, width=0.01, color=bar_color, edgecolor='none')

# === 拟合多个高斯峰 ===
for peak in fit_peaks:
    if not peak['show']:
        continue
    center = peak['center']
    half_range = peak['range'] / 2
    fit_mask = (x > center - half_range) & (x < center + half_range)
    x_fit = x[fit_mask]
    y_fit = y[fit_mask]

    try:
        popt, _ = curve_fit(gaussian, x_fit, y_fit, p0=[max(y_fit), center, 0.2])
        x_dense = np.linspace(-7, 1, 1000)
        y_dense = gaussian(x_dense, *popt)
        ax.plot(x_dense, y_dense, color=peak['color'], linewidth=0.4, label=peak['label'])

        ax.fill_between(x_dense, y_dense, color='#ffffff', alpha=0.4)
        fwhm = 2.35482 * popt[2]  # 计算半峰宽
        print(f"峰 {peak['label']}： μ={popt[1]:.4f}, a={popt[0]:.1f}, σ={popt[2]:.4f}, FWHM={fwhm:.4f}")
    except Exception as e:
        print(f"峰 {peak['label']} 拟合失败：{e}")

plt.xticks(
    fontsize=font_size,
)
# === 坐标轴与图例设置 ===
ax.set_xlabel('Conductance / log(G/G$_0$)', fontname=x_axis_font, fontsize=font_size)
ax.set_ylabel('Counts', fontname=y_axis_font, fontsize=font_size)
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_xticks(np.linspace(-6, 0, 7))
ax.set_yticks([])  # 隐藏 y 轴刻度
ax.tick_params(axis='y', which='both', length=0)  # 隐藏 y 轴刻度线

ax.grid(True, linestyle='--', alpha=0.0, linewidth=0.5)

fig.patch.set_alpha(0)  # 设置图像整体背景透明
ax.set_facecolor('none')  # 设置坐标轴区域背景透明

plt.show()
# plt.savefig("1d.png", dpi=300, transparent=True)