import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# -----------------------------
# Time setup
# -----------------------------
t = np.linspace(0, 5, 2000)   # 5 seconds
T = 1.0                       # heartbeat period

# -----------------------------
# Pulse function (periodic)
# -----------------------------
def pulse(t, c, w, a):
    return a * np.exp(-((np.mod(t, T) - c) ** 2) / (2 * w ** 2))

# -----------------------------
# Activation signals
# -----------------------------
A_atria = pulse(t, 0.2, 0.03, 0.3)

Q = pulse(t, 0.45, 0.01, -0.3)
R = pulse(t, 0.50, 0.02, 1.5)
S = pulse(t, 0.55, 0.015, -0.6)
A_vent = Q + R + S

A_repol = pulse(t, 0.75, 0.05, 0.4)

# -----------------------------
# Directions
# -----------------------------
d_atria = np.array([0.5, 1.0])
d_vent  = np.array([1.0, 0.2])
d_repol = np.array([0.6, 0.4])

# -----------------------------
# Cardiac vector
# -----------------------------
Ex = A_atria*d_atria[0] + A_vent*d_vent[0] + A_repol*d_repol[0]
Ey = A_atria*d_atria[1] + A_vent*d_vent[1] + A_repol*d_repol[1]

# -----------------------------
# ECG Leads
# -----------------------------
lead1 = np.array([1, 0])
lead2 = np.array([0.5, np.sqrt(3)/2])
lead3 = np.array([-0.5, np.sqrt(3)/2])

V1 = Ex*lead1[0] + Ey*lead1[1]
V2 = Ex*lead2[0] + Ey*lead2[1]
V3 = Ex*lead3[0] + Ey*lead3[1]

# -----------------------------
# Create figure with 2 plots
# -----------------------------
fig, (ax_vec, ax_ecg) = plt.subplots(2, 1, figsize=(6,8))

# --- Vector plot setup ---
ax_vec.set_xlim(-2, 2)
ax_vec.set_ylim(-2, 2)
ax_vec.set_aspect('equal')
ax_vec.grid()
ax_vec.set_title("Cardiac Vector")

# Plot leads
ax_vec.plot([0, lead1[0]], [0, lead1[1]], 'r--', label="Lead I")
ax_vec.plot([0, lead2[0]], [0, lead2[1]], 'g--', label="Lead II")
ax_vec.plot([0, lead3[0]], [0, lead3[1]], 'b--', label="Lead III")
ax_vec.legend()

vector_line, = ax_vec.plot([], [], 'k-', linewidth=3)

# --- ECG plot setup ---
ax_ecg.set_xlim(0, 5)
ax_ecg.set_ylim(min(V2)-0.5, max(V2)+0.5)
ax_ecg.set_title("ECG (Lead II)")
ax_ecg.set_xlabel("Time")
ax_ecg.set_ylabel("Voltage")
ax_ecg.grid()

ecg_line, = ax_ecg.plot([], [], 'g', linewidth=2)

# -----------------------------
# Animation function
# -----------------------------
def update(frame):
    # Update vector
    vector_line.set_data([0, Ex[frame]], [0, Ey[frame]])
    
    # Update ECG (progressively)
    ecg_line.set_data(t[:frame], V2[:frame])
    
    return vector_line, ecg_line

# -----------------------------
# Animate
# -----------------------------
ani = FuncAnimation(fig, update, frames=len(t), interval=5)

plt.tight_layout()
plt.show()