import os
import sys
import math

# omega_file = 'BTE.omega_full'   # radial frequency
# vel_file = 'BTE.v_full'         # group velocity
omega_file = 'BTE.omega'  # radial frequency
vel_file = 'BTE.v'  # group velocity

# =========
# READ DATA
# =========

omega = open(omega_file)  # omega
omega_data = omega.read().split('\n')
omega.close()
vel = open(vel_file)  # velocity
vel_data = vel.read().split('\n')
vel.close()

# ===========
# OUTPUT DATA
# ===========

NK = len(omega_data) - 1
nband = len(omega_data[0].split())
N = NK * nband


class DATA:
    def __init__(self, omega, vel_x, vel_y, vel_z):
        self.omega = float(omega) / 2 / math.pi  # rad/ps --> THz
        self.vel_x = abs(float(vel_x))
        self.vel_y = abs(float(vel_y))
        self.vel_z = abs(float(vel_z))
        self.vel = math.sqrt(self.vel_x ** 2 + self.vel_y ** 2 + self.vel_z ** 2)


data = []

for i in range(1, NK):
    omega = omega_data[i].split()
    vel = vel_data[i].split()

    # 检查 vel 列表是否有足够的数据
    if len(vel) < 3 * nband:
        print(f"Warning: Not enough velocity data for NK={i}")
        continue

    for j in range(0, nband):
        try:
            data.append(DATA(
                omega[j],  # omega
                vel[j + 0 * nband],  # vx
                vel[j + 1 * nband],  # vy
                vel[j + 2 * nband]  # vz
            ))
        except IndexError:
            print(f"IndexError: Not enough data for band {j} at NK={i}")
            continue

# 按 omega 排序
data.sort(key=lambda data: data.omega)

# 输出数据
print('#freq vx vy vz vel')
for i in range(0, len(data)):
    print(data[i].omega, data[i].vel_x, data[i].vel_y, data[i].vel_z, data[i].vel)
