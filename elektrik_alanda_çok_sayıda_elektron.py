# -*- coding: utf-8 -*-
"""Elektrik Alanda Çok Sayıda Elektron

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1br9tkWMnVMgJH5j2LhEl22xkGfmpdCDh
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
import matplotlib.animation as animation


#sabitler
q = 1.6 * 10**-19 #C
m = 9.1 * 10**-31 #kg
TIME_SPAN = [0, 10**-6] #s

#csv dosyasından data okuma (her 25 data pointten birini alıyoruz)
data = pd.read_csv("e-field_5.csv")
x = data['x'].values[::25]
y = data['y'].values[::25]
z = data['z'].values[::25]
E_x = data["E_x"].values[::25]
E_y = data['E_y'].values[::25]
E_z = data["E_z"].values[::25] ###unique yap###

#datayı interpolate etme
interp_Ex = scipy.interpolate.LinearNDInterpolator(list(zip(x, y, z)), E_x)
interp_Ey = scipy.interpolate.LinearNDInterpolator(list(zip(x, y, z)), E_y)
interp_Ez = scipy.interpolate.LinearNDInterpolator(list(zip(x, y, z)), E_z)

print("Interpolation completed")

def electric_field_at_point(r):
    Ex = interp_Ex(r)
    Ey = interp_Ey(r)
    Ez = interp_Ez(r)

    if np.isscalar(Ex) and np.isscalar(Ey) and np.isscalar(Ez):
        return np.array([Ex, Ey, Ez])
    else:
        return np.array([Ex.item(), Ey.item(), Ez.item()])

#diferansiyel denklem fonksiyonu
def diff(t, y):
    position = y[:3]
    velocity = y[3:]

    E_field = electric_field_at_point(position)
    acceleration = (q / m) * E_field

    return np.concatenate([velocity, acceleration])

#elektron sayısı ve başlangıç koşulları (hız dağılımı: normal dağılım)
num_electrons = 25
initial_positions = np.zeros((num_electrons, 3))
initial_velocities = np.random.normal(loc=[0,0,0], scale=1000, size=(num_electrons, 3))
INITIAL_CONDITIONS_LIST = [np.concatenate([initial_positions[i], initial_velocities[i]]) for i in range(num_electrons)]

#diferansiyel denklemin çözümü
solutions = []
X = []

for initial_conditions in INITIAL_CONDITIONS_LIST:
    solution = scipy.integrate.solve_ivp(diff, TIME_SPAN, initial_conditions, method="RK45", t_eval=np.linspace(TIME_SPAN[0], TIME_SPAN[1], 1000))
    solutions.append(solution)
    print(f"Completed {len(solutions)} out of {num_electrons} solutions")
    X.append(solution.y[0]) ###Dosyaya kaydedilsin

#3d çizim
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#plotun ayarları
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_zlim(-5, 5)
ax.set_xlabel('X position (m)')
ax.set_ylabel('Y position (m)')
ax.set_zlabel('Z position (m)')
ax.set_title("Electron Beam Trajectory in 3D")
ax.grid(True)

#animasyon için farklı renkler
colors = plt.cm.viridis(np.linspace(0, 1, num_electrons))

lines = []
for color in colors:
    line, = ax.plot([], [], [], '-', color=color, linewidth=0.5)
    lines.append(line)

#animasyon
def init():
    for line in lines:
        line.set_data([], [])
        line.set_3d_properties([])
    return lines

def animate(i):
    all_x = []
    all_y = []
    all_z = []
    for j, solution in enumerate(solutions):
        R_x = solution.y[0]
        R_y = solution.y[1]
        R_z = solution.y[2]
        lines[j].set_data(R_x[:i+1], R_y[:i+1])
        lines[j].set_3d_properties(R_z[:i+1])
        all_x.extend(R_x[:i+1])
        all_y.extend(R_y[:i+1])
        all_z.extend(R_z[:i+1])
        epsilon = 1e-9  #identical limits sorun çıkarabildiği için küçük bir epsilon değeri eklendi
        ax.set_xlim(min(all_x), max(all_x) + epsilon)
        ax.set_ylim(min(all_y), max(all_y) + epsilon)
        ax.set_zlim(min(all_z), max(all_z) + epsilon)

    return lines

ani = animation.FuncAnimation(fig, animate, init_func=init, frames=500, interval=20, blit=True)

ani.save('electron_beam_trajectory_1.mp4', writer='ffmpeg', fps=30, dpi = 150)

plt.show()


djghasdkgsd

