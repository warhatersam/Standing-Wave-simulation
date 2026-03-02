# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button


L = 1.0          # string length
c = 1.0          # base wave speed
N = 5            # number of standing waves
nx = 800
x = np.linspace(0, L, nx)

# Precompute mode shapes and angular frequencies
n = np.arange(1, N + 1)                           # 1..N
k = n * np.pi / L
w = c * k   #angular velocity for each standing wave

modes = np.sin(k[:, None] * x[None, :])           # shape: (N, nx)


fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.4)  # space for sliders

ax.set_title("Standing wave superposition")
ax.set_xlabel("x")
ax.set_ylabel("y(x,t)")
ax.set_xlim(0, L)
ax.set_ylim(-2.5, 2.5)

(line,) = ax.plot(x, np.zeros_like(x), lw=2)

# -------------------------
# Sliders for amplitudes A_n
# -------------------------
sliders = []
A0 = np.zeros(N)
A0[0] = 1.0  # start with fundamental on

slider_left = 0.12
slider_width = 0.78
slider_height = 0.03
slider_gap = 0.01
base_y = 0.2

for i in range(N):
    ax_slider = fig.add_axes([slider_left, base_y - i*(slider_height + slider_gap),
                              slider_width, slider_height])
    s = Slider(
        ax=ax_slider,
        label=f"{i+1}00Hz",
        valmin=0.0,
        valmax=2.0,
        valinit=A0[i],
        valstep=0.01
    )
    sliders.append(s)

# Optional: speed slider (controls how fast time advances)
ax_speed = fig.add_axes([0.12, 0.25, 0.50, 0.03])
speed_slider = Slider(ax_speed, "speed", 0.0, 3.0, valinit=1.0, valstep=0.01)

# Play/pause button
ax_btn = fig.add_axes([0.70, 0.3, 0.20, 0.05])
btn = Button(ax_btn, "Pause")
running = {"on": True}

def toggle(event):
    running["on"] = not running["on"]
    btn.label.set_text("Pause" if running["on"] else "Play")

btn.on_clicked(toggle)

# -------------------------
# Animation
# -------------------------
t = 0.0
dt = 1/60  # base timestep (seconds per frame)

def compute_y(t_now):
    # Read amplitudes from sliders
    A = np.array([s.val for s in sliders])
    # y(x,t) = sum_n A_n sin(k_n x) cos(w_n t)
    cos_part = np.cos(w * t_now)
    # Combine: sum over n of (A_n * cos(w_n t) * mode_n(x))
    return (A * cos_part) @ modes            # (N,) @ (N,nx) -> (nx,)

def update(frame):
    global t
    if running["on"]:
        t += dt * speed_slider.val
    y = compute_y(t)
    line.set_ydata(y)

    # Auto-scale y-limits a bit (optional)
    y_max = max(0.5, 1.1 * np.max(np.abs(y)))
    ax.set_ylim(-y_max, y_max)
    return (line,)

ani = FuncAnimation(fig, update, interval=16, blit=True, cache_frame_data=False)
plt.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
