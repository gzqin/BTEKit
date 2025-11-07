import math

omega_file = 'BTE.omega'
vel_file = 'BTE.v'

# 读入数据
with open(omega_file) as f:
    omega_data = [float(x) for x in f.read().split() if x.strip()]

with open(vel_file) as f:
    vel_data = [list(map(float, x.split())) for x in f.read().splitlines() if x.strip()]

if len(omega_data) != len(vel_data):
    print(f"Warning: length mismatch between omega ({len(omega_data)}) and velocity ({len(vel_data)})")

class Data:
    def __init__(self, omega, vx, vy, vz):
        # 单位：rad/ps -> THz
        self.freq = float(omega) / (2 * math.pi)
        self.vx = abs(float(vx))
        self.vy = abs(float(vy))
        self.vz = abs(float(vz))
        self.vel = math.sqrt(self.vx**2 + self.vy**2 + self.vz**2)

# 逐行匹配
data = [Data(o, *v) for o, v in zip(omega_data, vel_data)]

# 按频率排序
data.sort(key=lambda d: d.freq)

# 输出结果
print("#freq(THz)  vx  vy  vz  |v|")
for d in data[:10]:  # 仅预览前10行
    print(f"{d.freq:.4f}  {d.vx:.3e}  {d.vy:.3e}  {d.vz:.3e}  {d.vel:.3e}")

# 保存到文件
with open("freq_velocity.dat", "w") as f:
    f.write("#freq(THz)  vx  vy  vz  |v|\n")
    for d in data:
        f.write(f"{d.freq:.6f}  {d.vx:.6e}  {d.vy:.6e}  {d.vz:.6e}  {d.vel:.6e}\n")

print("✅ 输出已保存至 freq_velocity.dat")
