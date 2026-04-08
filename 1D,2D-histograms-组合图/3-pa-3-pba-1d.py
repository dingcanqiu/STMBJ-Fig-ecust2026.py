import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.ndimage import gaussian_filter1d

# === 确保全局全部使用 Arial 字体 ===
plt.rcParams["font.family"] = "Arial"

# ===========================
#        高斯函数
# ===========================
def gaussian(x, a, mu, sigma):
    return a * np.exp(-((x - mu)**2) / (2 * sigma**2))

def fwhm_from_sigma(sigma):
    return 2 * np.sqrt(2 * np.log(2)) * sigma

# ===========================
#        图像基本参数
# ===========================
x_axis_font = 'Arial'
y_axis_font = 'Arial'
font_size = 12

x_min, x_max = -6.5, 0.5

# 物理尺寸（英寸）
x_axis_inches = 2.5
y_axis_inches = 2.3
left_margin = 0.7
right_margin = 0.3
top_margin = 0.3
bottom_margin = 0.5
middle_gap = 0.0   # 两图之间距离

fig_width = left_margin + x_axis_inches + right_margin
fig_height = bottom_margin + 2 * y_axis_inches + top_margin + middle_gap

# 创建整体画布
fig = plt.figure(figsize=(fig_width, fig_height), dpi=100)

# 使用 gridspec 进行上下布局
import matplotlib.gridspec as gridspec
gs = gridspec.GridSpec(
    2, 1,
    height_ratios=[1, 1],
    hspace=middle_gap / fig_height
)

# ===========================
#        第 1 个图（上）
# ===========================
ax1 = fig.add_axes([
    left_margin / fig_width,
    (bottom_margin + y_axis_inches + middle_gap) / fig_height,
    x_axis_inches / fig_width,
    y_axis_inches / fig_height
])

# === 读取数据1 ===
data1 = np.loadtxt('D:/Python/pycharm/nas/1D,2D-histograms-组合图/3-pa/WA-BJ_logHist.txt')
x1, y1 = data1[:, 0], data1[:, 1]

# === 绘制直方图 ===
ax1.bar(x1, y1, width=0.01, color='#BBDFC9', edgecolor='none')

# === 第1图的拟合 ===
fit_peaks_1 = [
    {'center': -2.5, 'range': 0.5, 'show': True,  'color': '#000000',  'label': 'HC'},
    {'center': -4.0, 'range': 0.6, 'show': False, 'color': '#000000', 'label': 'LC'},
]

y1_smooth = gaussian_filter1d(y1, sigma=1.5)

for peak in fit_peaks_1:
    if not peak["show"]:
        continue

    center = peak['center']
    half_range = peak['range'] / 2
    fit_mask = (x1 > center - half_range) & (x1 < center + half_range)

    x_fit = x1[fit_mask]
    y_fit = y1_smooth[fit_mask]
    weights = 1 / (np.sqrt(y_fit) + 1e-3)

    sigma0 = 0.12
    bounds_lower = [0, center - 0.2, 0.1]
    bounds_upper = [np.inf, center + 0.2, 1.4]


    popt, _ = curve_fit(
        gaussian, x_fit, y_fit,
        p0=[max(y_fit), center, sigma0],
        bounds=(bounds_lower, bounds_upper),
        sigma=weights
    )
    peak_height = popt[0]
    peak_center = popt[1]
    peak_sigma = popt[2]
    peak_fwhm = 2 * np.sqrt(2 * np.log(2)) * peak_sigma

    print(f"[Top panel] {peak['label']} peak:")
    print(f"  Center = {peak_center:.3f}")
    print(f"  Sigma  = {peak_sigma:.3f}")
    print(f"  FWHM   = {peak_fwhm:.3f}")
    print(f"  Peak height = {peak_height:.1f}")

    x_dense = np.linspace(-7, 1, 1000)
    y_dense = gaussian(x_dense, *(popt[0] * 1, popt[1], popt[2]))
    ax1.plot(x_dense, y_dense, color=peak['color'], linewidth=0.4)
    ax1.fill_between(x_dense, y_dense, color='#ffffff', alpha=0.4)

# === 坐标设置 ===
ax1.set_xlim(x_min, x_max)
ax1.set_ylim(0, 3000)
# 隐藏上图的 x 轴
ax1.set_xticks([])                 # 取消刻度
ax1.tick_params(axis='x', length=0)  # 取消刻度线
ax1.set_xlabel("")                 # 确保无 x 轴标签
ax1.spines['bottom'].set_visible(False)  # 隐藏下边轴线
ax1.set_yticks([])

ax1.tick_params(axis='y', length=0)
ax1.grid(True, linestyle='--', linewidth=0.2, alpha=0.0)
ax1.set_facecolor('none')


# ===========================
#        第 2 个图（下）
# ===========================
ax2 = fig.add_axes([
    left_margin / fig_width,
    bottom_margin / fig_height,
    x_axis_inches / fig_width,
    y_axis_inches / fig_height
])

# === 读取数据2 ===
data2 = np.loadtxt('D:/Python/pycharm/nas/1D,2D-histograms-组合图/3-pba/WA-BJ_logHist.txt')
x2, y2 = data2[:, 0], data2[:, 1]

# === 绘制直方图 ===
ax2.bar(x2, y2, width=0.01, color='#9ec8b0', edgecolor='none')

# === 第2图的拟合 ===
fit_peaks_2 = [
    {'center': -3.7, 'range': 0.6, 'show': True, 'color': '#000000', 'label': 'MC'},
    {'center': -5.0, 'range': 0.6, 'show': True, 'color': '#000000', 'label': 'LC'},
]

for peak in fit_peaks_2:
    if not peak["show"]:
        continue

    center = peak['center']
    half_range = peak['range'] / 2
    fit_mask = (x2 > center - half_range) & (x2 < center + half_range)
    x_fit = x2[fit_mask]
    y_fit = y2[fit_mask]

    sigma0 = 0.18 if peak['label'] == "MC" else 0.10
    bounds_lower = [0, center - 0.2, 0.08]
    bounds_upper = [np.inf, center + 0.2, 1.8]

    popt, _ = curve_fit(
        gaussian, x_fit, y_fit,
        p0=[max(y_fit), center, sigma0],
        bounds=(bounds_lower, bounds_upper)
    )
    peak_height = popt[0]
    peak_center = popt[1]

    print(f"[Top panel] {peak['label']} peak:")
    print(f"  Center = {peak_center:.3f}")
    print(f"  Peak height = {peak_height:.1f}")

    x_dense = np.linspace(-7, 1, 1000)
    y_dense = gaussian(x_dense, *(popt[0], popt[1], popt[2]))
    ax2.plot(x_dense, y_dense, color=peak['color'], linewidth=0.4)
    ax2.fill_between(x_dense, y_dense, color='#ffffff', alpha=0.4)

# === 坐标设置 ===
ax2.set_xlim(x_min, x_max)
ax2.set_ylim(0, 6000)
ax2.set_xticks(np.linspace(-6, 0, 7))
ax2.set_xlabel('Conductance / log(G/G$_0$)', fontname=x_axis_font, fontsize=font_size)
ax2.set_yticks([])
ax2.tick_params(axis='x', labelsize=12)   # 10 是字体大小
ax2.tick_params(axis='y', length=0)
ax2.grid(True, linestyle='--', linewidth=0.2, alpha=0.0)
ax2.set_facecolor('none')

# 整体背景透明
fig.patch.set_alpha(0)
# ---- 计算共享 y 轴标题应当放置的位置（上下图坐标轴的中点） ----

ax1_y0 = (bottom_margin + y_axis_inches + middle_gap) / fig_height
ax1_h  = y_axis_inches / fig_height

ax2_y0 = bottom_margin / fig_height
ax2_h  = y_axis_inches / fig_height

# 两个 y 坐标轴的垂直中点
y_center = (ax1_y0 + (ax2_y0 + ax2_h)) / 2

# ---- 添加 y 轴标题 ----
fig.text(
    (left_margin - 0.26) / fig_width,      # x 位置（可微调）
    y_center,
    'Counts',
    fontname=y_axis_font,
    fontsize=font_size,
    rotation='vertical',
    va='center'
)


plt.show()
# plt.savefig("1d-squ.png", dpi=300, transparent=True)