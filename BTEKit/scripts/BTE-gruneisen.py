import numpy as np
import matplotlib.pyplot as plt

# ======== 文件路径 ========
omega_file = "BTE.omega"          # 频率（rad/ps）
gruneisen_file = "BTE.gruneisen"  # 格吕奈森参数 γ

# ======== 读取数据 ========
omega_data = np.loadtxt(omega_file)
gruneisen_data = np.loadtxt(gruneisen_file)

# 确保维度匹配
if omega_data.shape != gruneisen_data.shape:
    raise ValueError("omega 与 gruneisen 文件维度不匹配！")

nq, nb = omega_data.shape  # nq点数, 声子带数

# ======== 转换单位 ========
omega_THz = omega_data / (2 * np.pi)  # rad/ps → THz

# ======== 扁平化为 1D 数组 ========
omega_flat = omega_THz.flatten()
gruneisen_flat = gruneisen_data.flatten()

# ======== 分声学/光学模式区分 ========
# 简单假设：前三支为声学模
acoustic = np.tile(np.arange(nb) < 3, nq)
optical = ~acoustic

# ======== 绘图 ========
plt.figure(figsize=(8, 6))

plt.scatter(
    omega_flat[acoustic],
    gruneisen_flat[acoustic],
    s=15,
    color="royalblue",
    alpha=0.6,
    label="Acoustic modes"
)
plt.scatter(
    omega_flat[optical],
    gruneisen_flat[optical],
    s=15,
    color="tomato",
    alpha=0.6,
    label="Optical modes"
)

# ======== 美化 ========
plt.title("Phonon Grüneisen Parameters", fontsize=14, fontweight="bold")
plt.xlabel("Frequency (THz)", fontsize=12)
plt.ylabel("Grüneisen Parameter γ", fontsize=12)
plt.legend(frameon=True)
plt.grid(alpha=0.3, linestyle="--")
plt.tight_layout()

# 保存结果
plt.savefig("gruneisen_colored.png", dpi=300)
plt.show()

print("✅ 绘图完成，结果已保存为 gruneisen_colored.png")
